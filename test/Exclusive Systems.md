Bevy Version:0.9(outdated!)


Exclusive Systems
Exclusive systems are systems that Bevy will not run in parallel
with any other system. They can have full unrestricted access
to the whole ECS World, by taking a &mut World parameter.
Inside of an exclusive system, you have full control over all data stored
in the ECS. You can do whatever you want.
Note that exclusive systems can limit performance, as they prevent
multi-threading (nothing else runs at the same time).
Some example situations where exclusive systems are useful:

Dump various entities and components to a file, to implement things like
saving and loading of game save files, or scene export from an editor
Directly spawn/despawn entities, or create/remove resources,
immediately with no delay (unlike when using Commands
from a regular system)
Run arbitrary systems with your own scheduling algorithm
…

See the direct World access page to learn more about how to do
such things.
fn do_crazy_things(world: &mut World) {
    // we can do anything with any data in the Bevy ECS here!
}
You need to add exclusive systems to the App, just like
regular systems, but you must call .exclusive_system() on them.
They cannot be ordered in-between regular parallel systems. Exclusive systems
always run at one of the following places:

.at_start(): at the beginning of a stage
.at_end(): at the end of a stage,
after commands from regular systems have been applied
.before_commands(): after all the regular systems in a stage,
but before commands are applied

(if you don't specify anything, the default is assumed .at_start())
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)

        // this will run at the start of CoreStage::Update (the default stage)
        .add_system(do_crazy_things)

        // this will run at the end of CoreStage::PostUpdate
        .add_system_to_stage(
            CoreStage::PostUpdate,
            some_more_things
                .at_end()
        )

        .run();
}

### References
[[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 