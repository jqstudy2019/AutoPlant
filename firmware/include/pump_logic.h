#pragma once
// Pure pump-permission logic, no Arduino headers, so it unit-tests on the host.
#include <cstdint>

namespace pump {

constexpr uint32_t MAX_RUNTIME_MS   = 30000;   // DI-08
constexpr uint32_t LINK_TIMEOUT_MS  = 120000;  // DI-11: no supervisor message for 2 min

struct Inputs {
    bool     reservoir_low;     // DI-09
    uint32_t now_ms;
    uint32_t last_link_ms;      // last valid message from supervisor
    uint32_t started_ms;        // when the current run began
    uint32_t requested_ms;      // duration the supervisor asked for
    bool     running;
};

// Clamp a requested run to the firmware limit.
inline uint32_t clamp_runtime(uint32_t requested_ms) {
    return requested_ms > MAX_RUNTIME_MS ? MAX_RUNTIME_MS : requested_ms;
}

inline bool link_ok(const Inputs& in) {
    return (in.now_ms - in.last_link_ms) <= LINK_TIMEOUT_MS;  // wrap-safe for uint32
}

// May a new run start?
inline bool may_start(const Inputs& in) {
    return !in.reservoir_low && link_ok(in);
}

// Must a running pump stop now?
inline bool must_stop(const Inputs& in) {
    if (!in.running) return false;
    const uint32_t elapsed = in.now_ms - in.started_ms;
    return in.reservoir_low
        || !link_ok(in)
        || elapsed >= clamp_runtime(in.requested_ms);
}

}  // namespace pump
