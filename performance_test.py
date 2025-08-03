#!/usr/bin/env python
"""
메모짱 성능 테스트 스크립트
"""
import os
import sys
import django
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memojjang.settings')
django.setup()

# 테스트를 위해 ALLOWED_HOSTS 설정
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client
from django.contrib.auth.models import User
from apps.memos.models import Memo


class PerformanceTester:
    def __init__(self):
        self.client = Client()
        self.setup_test_data()
        
    def setup_test_data(self):
        """테스트 데이터 설정"""
        # 테스트 사용자 생성
        self.user, created = User.objects.get_or_create(
            username='perftest_user',
            defaults={'password': 'testpass123'}
        )
        
        # 기존 테스트 메모 삭제
        Memo.objects.filter(author=self.user).delete()
        
        # 대량 메모 생성 (성능 테스트용)
        print("테스트 데이터 생성 중...")
        memos = []
        for i in range(1000):
            memo = Memo(
                title=f'Performance Test Memo {i+1}',
                content=f'This is a performance test memo content. ' * 20,
                author=self.user,
                priority=['low', 'normal', 'high', 'urgent'][i % 4],
                is_pinned=(i % 10 == 0)
            )
            memos.append(memo)
        
        Memo.objects.bulk_create(memos, batch_size=100)
        print(f"✅ {len(memos)}개의 테스트 메모 생성 완료")
        
    def measure_response_time(self, url, params=None):
        """응답 시간 측정"""
        start_time = time.time()
        response = self.client.get(url, params or {})
        end_time = time.time()
        
        return {
            'response_time': end_time - start_time,
            'status_code': response.status_code,
            'content_length': len(response.content)
        }
    
    def test_memo_list_performance(self, iterations=10):
        """메모 목록 성능 테스트"""
        print(f"\n🔍 메모 목록 성능 테스트 ({iterations}회 반복)")
        
        # 로그인
        self.client.force_login(self.user)
        
        response_times = []
        for i in range(iterations):
            result = self.measure_response_time('/memos/')
            response_times.append(result['response_time'])
            print(f"  {i+1:2d}. {result['response_time']:.3f}초 (상태: {result['status_code']})")
        
        # 통계 계산
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"\n📊 메모 목록 성능 결과:")
        print(f"   평균: {avg_time:.3f}초")
        print(f"   최소: {min_time:.3f}초")
        print(f"   최대: {max_time:.3f}초")
        
        return {
            'avg': avg_time,
            'min': min_time,
            'max': max_time
        }
    
    def test_search_performance(self, iterations=10):
        """검색 성능 테스트"""
        print(f"\n🔍 검색 성능 테스트 ({iterations}회 반복)")
        
        search_queries = [
            'Performance',
            'Test',
            'Memo',
            'content',
            '1'
        ]
        
        all_times = []
        
        for query in search_queries:
            print(f"\n  검색어: '{query}'")
            response_times = []
            
            for i in range(iterations):
                result = self.measure_response_time(
                    '/memos/search/ajax/', 
                    {'q': query}
                )
                response_times.append(result['response_time'])
                print(f"    {i+1:2d}. {result['response_time']:.3f}초")
            
            avg_time = statistics.mean(response_times)
            all_times.extend(response_times)
            print(f"    평균: {avg_time:.3f}초")
        
        # 전체 통계
        overall_avg = statistics.mean(all_times)
        print(f"\n📊 검색 성능 전체 결과:")
        print(f"   전체 평균: {overall_avg:.3f}초")
        
        return overall_avg
    
    def test_concurrent_access(self, concurrent_users=5, requests_per_user=5):
        """동시 접속 성능 테스트"""
        print(f"\n🚀 동시 접속 테스트 ({concurrent_users}명, 각 {requests_per_user}회 요청)")
        
        def make_requests(user_id):
            """각 사용자가 수행할 요청"""
            client = Client()
            client.force_login(self.user)
            
            times = []
            for i in range(requests_per_user):
                start_time = time.time()
                response = client.get('/memos/')
                end_time = time.time()
                
                times.append(end_time - start_time)
            
            return times
        
        # 동시 실행
        all_times = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [
                executor.submit(make_requests, i) 
                for i in range(concurrent_users)
            ]
            
            for future in as_completed(futures):
                user_times = future.result()
                all_times.extend(user_times)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 결과 분석
        avg_response_time = statistics.mean(all_times)
        total_requests = concurrent_users * requests_per_user
        requests_per_second = total_requests / total_time
        
        print(f"\n📊 동시 접속 테스트 결과:")
        print(f"   총 요청 수: {total_requests}")
        print(f"   총 소요 시간: {total_time:.3f}초")
        print(f"   평균 응답 시간: {avg_response_time:.3f}초")
        print(f"   초당 요청 수: {requests_per_second:.1f} RPS")
        
        return {
            'total_requests': total_requests,
            'total_time': total_time,
            'avg_response_time': avg_response_time,
            'requests_per_second': requests_per_second
        }
    
    def test_database_queries(self):
        """데이터베이스 쿼리 성능 테스트"""
        print(f"\n💾 데이터베이스 쿼리 성능 테스트")
        
        from django.db import connection
        from django.test.utils import override_settings
        
        # 쿼리 로깅 활성화
        with override_settings(DEBUG=True):
            connection.queries_log.clear()
            
            # 메모 목록 페이지 요청
            self.client.force_login(self.user)
            response = self.client.get('/memos/')
            
            # 쿼리 분석
            queries = connection.queries
            total_time = sum(float(q['time']) for q in queries)
            
            print(f"   실행된 쿼리 수: {len(queries)}")
            print(f"   총 쿼리 시간: {total_time:.3f}초")
            if len(queries) > 0:
                print(f"   평균 쿼리 시간: {total_time/len(queries):.3f}초")
            else:
                print("   쿼리가 실행되지 않았습니다.")
            
            # 느린 쿼리 찾기
            slow_queries = [q for q in queries if float(q['time']) > 0.01]
            if slow_queries:
                print(f"   느린 쿼리 ({len(slow_queries)}개):")
                for q in slow_queries[:3]:  # 상위 3개만 표시
                    print(f"     {float(q['time']):.3f}초: {q['sql'][:100]}...")
        
        return {
            'query_count': len(queries),
            'total_time': total_time,
            'slow_queries': len(slow_queries) if 'slow_queries' in locals() else 0
        }
    
    def run_all_tests(self):
        """모든 성능 테스트 실행"""
        print("🎯 메모짱 성능 테스트 시작")
        print("=" * 50)
        
        # 각 테스트 실행
        list_results = self.test_memo_list_performance()
        search_results = self.test_search_performance()
        concurrent_results = self.test_concurrent_access()
        db_results = self.test_database_queries()
        
        # 종합 결과
        print("\n" + "=" * 50)
        print("📊 종합 성능 테스트 결과")
        print("=" * 50)
        
        print(f"메모 목록 평균 응답시간: {list_results['avg']:.3f}초")
        print(f"검색 평균 응답시간: {search_results:.3f}초")
        print(f"동시 접속 처리량: {concurrent_results['requests_per_second']:.1f} RPS")
        print(f"데이터베이스 쿼리 수: {db_results['query_count']}개")
        
        # 성능 등급 판정
        if list_results['avg'] < 0.5:
            print("✅ 성능 등급: 우수")
        elif list_results['avg'] < 1.0:
            print("⚠️  성능 등급: 보통")
        else:
            print("❌ 성능 등급: 개선 필요")
        
        # 정리
        print(f"\n🧹 테스트 데이터 정리...")
        Memo.objects.filter(author=self.user).delete()
        print("✅ 정리 완료")


if __name__ == '__main__':
    tester = PerformanceTester()
    tester.run_all_tests()
