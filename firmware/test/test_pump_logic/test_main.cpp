// Host unit tests for pump permission logic (supports VER-06, VER-07).
// Run with: pio test -e native
#include <unity.h>
#include "../../include/pump_logic.h"

using namespace pump;

static Inputs base() { return Inputs{false, 1000, 1000, 1000, 10000, true}; }

void test_clamps_long_request() { TEST_ASSERT_EQUAL_UINT32(MAX_RUNTIME_MS, clamp_runtime(120000)); }

void test_stops_at_requested_time() {
    Inputs in = base();
    in.now_ms = in.started_ms + 9999;  TEST_ASSERT_FALSE(must_stop(in));
    in.now_ms = in.started_ms + 10000; TEST_ASSERT_TRUE(must_stop(in));
}

void test_stops_at_hard_limit_even_if_more_requested() {
    Inputs in = base(); in.requested_ms = 120000;
    in.now_ms = in.started_ms + MAX_RUNTIME_MS; in.last_link_ms = in.now_ms;
    TEST_ASSERT_TRUE(must_stop(in));
}

void test_reservoir_low_blocks_and_stops() {
    Inputs in = base(); in.reservoir_low = true;
    TEST_ASSERT_FALSE(may_start(in));
    TEST_ASSERT_TRUE(must_stop(in));
}

void test_link_loss_blocks_and_stops() {
    Inputs in = base(); in.now_ms = in.last_link_ms + LINK_TIMEOUT_MS + 1;
    TEST_ASSERT_FALSE(may_start(in));
    TEST_ASSERT_TRUE(must_stop(in));
}

void test_millis_wraparound() {
    Inputs in = base();
    in.started_ms = 0xFFFFF000u; in.last_link_ms = 0xFFFFF000u; in.now_ms = 0x00000100u;  // ~4.4 s later
    TEST_ASSERT_FALSE(must_stop(in));
}

int main() {
    UNITY_BEGIN();
    RUN_TEST(test_clamps_long_request);
    RUN_TEST(test_stops_at_requested_time);
    RUN_TEST(test_stops_at_hard_limit_even_if_more_requested);
    RUN_TEST(test_reservoir_low_blocks_and_stops);
    RUN_TEST(test_link_loss_blocks_and_stops);
    RUN_TEST(test_millis_wraparound);
    return UNITY_END();
}
