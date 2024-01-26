Bevy Version:0.9(outdated!)


Time and Timers
Relevant official examples:
timers,
move_sprite.

Time
The Time resource is your main global source
of timing information, that you can access from any system
that does anything that needs time. You should derive all timings from
it.
Bevy updates these values at the beginning of every frame.
Delta Time
The most common use case is "delta time" – how much time passed between
the previous frame update and the current one. This tells you how fast the
game is running, so you can scale things like movement and animations. This
way everything can happen smoothly and run at the same speed, regardless of
the game's frame rate.
fn asteroids_fly(
    time: Res<Time>,
    mut q: Query<&mut Transform, With<Asteroid>>,
) {
    for mut transform in q.iter_mut() {
        // move our asteroids along the X axis
        // at a speed of 10.0 units per second
        transform.translation.x += 10.0 * time.delta_seconds();
    }
}
Ongoing Time
Time can also give you the total running time since startup.
Use this if you need a cumulative, increasing, measurement of time.
use std::time::Instant;

/// Say, for whatever reason, we want to keep track
/// of when exactly some specific entities were spawned.
#[derive(Component)]
struct SpawnedTime(Instant);

fn spawn_my_stuff(
    mut commands: Commands,
    time: Res<Time>,
) {
    commands.spawn((/* ... */))
        // we can use startup time and elapsed duration
        .insert(SpawnedTime(time.startup() + time.elapsed()))
        // or just the time of last update
        .insert(SpawnedTime(time.last_update().unwrap()));
}
Timers and Stopwatches
There are also facilities to help you track specific intervals or timings:
Timer and Stopwatch. You can create
many instances of these, to track whatever you want. You can use them in
your own component or resource types.
Timers and Stopwatches need to be ticked. You need to have some system
calling .tick(delta), for it to make progress, or it will be inactive.
The delta should come from the Time resource.
Timer
Timer allows you to detect when a certain interval of time
has elapsed. Timers have a set duration. They can be "repeating" or
"non-repeating".
Both kinds can be manually "reset" (start counting the time interval from the
beginning) and "paused" (they will not progress even if you keep ticking them).
Repeating timers will automatically reset themselves after they reach their
set duration.
Use .finished() to detect when a timer has reached its set duration. Use
.just_finished(), if you need to detect only on the exact tick when the
duration was reached.
use std::time::Duration;

#[derive(Component)]
struct FuseTime {
    /// track when the bomb should explode (non-repeating timer)
    timer: Timer,
}

fn explode_bombs(
    mut commands: Commands,
    mut q: Query<(Entity, &mut FuseTime)>,
    time: Res<Time>,
) {
    for (entity, mut fuse_timer) in q.iter_mut() {
        // timers gotta be ticked, to work
        fuse_timer.timer.tick(time.delta());

        // if it finished, despawn the bomb
        if fuse_timer.timer.finished() {
            commands.entity(entity).despawn();
        }
    }
}

#[derive(Resource)]
struct BombsSpawnConfig {
    /// How often to spawn a new bomb? (repeating timer)
    timer: Timer,
}

/// Spawn a new bomb in set intervals of time
fn spawn_bombs(
    mut commands: Commands,
    time: Res<Time>,
    mut config: ResMut<BombsSpawnConfig>,
) {
    // tick the timer
    config.timer.tick(time.delta());

    if config.timer.finished() {
        commands.spawn((
            FuseTime {
                // create the non-repeating fuse timer
                timer: Timer::new(Duration::from_secs(5), TimerMode::Once),
            },
            // ... other components ...
        ));
    }
}

/// Configure our bomb spawning algorithm
fn setup_bomb_spawning(
    mut commands: Commands,
) {
    commands.insert_resource(BombsSpawnConfig {
        // create the repeating timer
        timer: Timer::new(Duration::from_secs(10), TimerMode::Repeating),
    })
}
Note that Bevy's timers do not work like typical real-life timers (which
count downwards toward zero). Bevy's timers start from zero and count up
towards their set duration. They are basically like stopwatches with extra
features: a maximum duration and optional auto-reset.
Stopwatch
Stopwatch allow you to track how much time has passed
since a certain point.
It will just keep accumulating time, which you can check with
.elapsed()/.elapsed_secs(). You can manually reset it at any time.
use bevy::time::Stopwatch;

#[derive(Component)]
struct JumpDuration {
    time: Stopwatch,
}

fn jump_duration(
    time: Res<Time>,
    mut q_player: Query<&mut JumpDuration, With<Player>>,
    kbd: Res<Input<KeyCode>>,
) {
    // assume we have exactly one player that jumps with Spacebar
    let mut jump = q_player.single_mut();

    if kbd.just_pressed(KeyCode::Space) {
        jump.time.reset();
    }

    if kbd.pressed(KeyCode::Space) {
        println!("Jumping for {} seconds.", jump.time.elapsed_secs());
        // stopwatch has to be ticked to progress
        jump.time.tick(time.delta());
    }
}

### References
[[Entities Components  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Jittering Time choppy movementanimation  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 