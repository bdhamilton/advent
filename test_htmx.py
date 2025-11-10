#!/usr/bin/env python3
"""Test script to verify HTMX endpoints work correctly"""

from app import app, ACTIVITIES, get_todays_activity
from datetime import date

def test_htmx_endpoints():
    """Test that the HTMX endpoints return partial HTML"""
    with app.test_client() as client:
        print("Testing HTMX implementation...")
        print("-" * 50)

        # Test 1: Toggle today's activity (no index)
        print("\n1. Testing today's activity toggle...")
        today_activity = get_todays_activity()
        response = client.post('/toggle-activity', data={
            'activity': today_activity
        })

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        html = response.data.decode('utf-8')

        # Should contain the form with today-activity-form id
        assert 'id="today-activity-form"' in html, "Missing today-activity-form id"
        assert 'hx-post="/toggle-activity"' in html, "Missing HTMX attributes"
        assert 'checked' in html, "Activity should be checked after toggle"
        print("   ✓ Today's activity toggle works")
        print(f"   ✓ Activity: {today_activity}")
        print(f"   ✓ Response length: {len(html)} bytes")

        # Test 2: Toggle an activity from the list (with index)
        print("\n2. Testing list activity toggle...")
        test_index = 0
        test_activity = ACTIVITIES[test_index]
        response = client.post('/toggle-activity', data={
            'activity': test_activity,
            'index': str(test_index)
        })

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        html = response.data.decode('utf-8')

        # Should contain the activity item div
        assert f'id="activity-item-{test_index}"' in html, f"Missing activity-item-{test_index} id"
        assert f'id="activity-form-{test_index}"' in html, f"Missing activity-form-{test_index} id"
        assert 'hx-post="/toggle-activity"' in html, "Missing HTMX attributes"
        assert test_activity in html, f"Missing activity text: {test_activity}"
        print("   ✓ List activity toggle works")
        print(f"   ✓ Activity: {test_activity}")
        print(f"   ✓ Response length: {len(html)} bytes")

        # Test 3: Verify main page renders
        print("\n3. Testing main page render...")
        response = client.get('/')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        html = response.data.decode('utf-8')
        assert 'htmx.org' in html, "HTMX library not included"
        assert 'hx-post' in html, "HTMX attributes not present"
        assert today_activity in html, "Today's activity not displayed"
        print("   ✓ Main page renders correctly")
        print(f"   ✓ Page contains HTMX library")
        print(f"   ✓ Page contains HTMX attributes")

        print("\n" + "-" * 50)
        print("✅ All HTMX tests passed!")
        return True

if __name__ == '__main__':
    try:
        test_htmx_endpoints()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
