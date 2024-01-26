Bevy Version:0.9(outdated!)


Fixed Timestep
Relevant official examples:
fixed_timestep.

If you need something to happen at fixed time intervals (a common use case
is Physics updates), you can add the respective systems to
your app using Bevy's FixedTimestep
Run Criteria.
use bevy::time::FixedTimestep;

// The timestep says how many times to run the SystemSet every second
// For TIMESTEP_1, it's once every second
// For TIMESTEP_2, it's twice every second

const TIMESTEP_1_PER_SECOND: f64 = 60.0 / 60.0;
const TIMESTEP_2_PER_SECOND: f64 = 30.0 / 60.0;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_system_set(
            SystemSet::new()
                // This prints out "hello world" once every second
                .with_run_criteria(FixedTimestep::step(TIMESTEP_1_PER_SECOND))
                .with_system(slow_timestep)
        )
        .add_system_set(
            SystemSet::new()
                // This prints out "goodbye world" twice every second
                .with_run_criteria(FixedTimestep::step(TIMESTEP_2_PER_SECOND))
                .with_system(fast_timestep)
        )
        .run();
}

fn slow_timestep() {
    println!("hello world");
}

fn fast_timestep() {
    println!("goodbye world");
}
State
You can check the current state of the fixed timestep trackers, by accessing
the FixedTimesteps resource. This lets
you know how much time remains until the next time it triggers, or how much
it has overstepped. You need to label your fixed timesteps.
See the official example, which illustrates this.
Caveats
The major problem with Bevy's fixed timestep comes from the fact that
it is implemented using Run Criteria. It cannot be
combined with other run criteria, such as states. This makes
it unusable for most projects, which need to rely on states for things
like implementing the main menu / loading screen / etc. Consider using
iyes_loopless, which does not have this problem.
Also, note that your systems are still called as part of the
regular frame-update cycle, along with all of the normal systems. So, the
timing is not exact.
The FixedTimestep run criteria simply checks how much
time passed since the last time your systems were ran, and decides whether
to run them during the current frame, or not, or run them multiple times,
as needed.
Danger! Lost events!
By default, Bevy's events are not reliable! They only persist
for 2 frames, after which they are lost. If your fixed-timestep systems
receive events, beware that you may miss some events if the framerate is
higher than 2x the fixed timestep.
One way around that is to use events with manual
clearing. This gives you control over how long events
persist, but can also leak / waste memory if you forget to clear them.

### References
[[Manual Event Clearing  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 