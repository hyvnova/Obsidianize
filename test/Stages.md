Bevy Version:0.9(outdated!)


Stages
All systems to be run by Bevy are contained in stages. Every
frame update, Bevy executes each stage, in order. Within each stage, Bevy's
scheduling algorithm can run many systems in parallel, using multiple CPU
cores for good performance.
The boundaries between stages are effectively hard synchronization points.
They ensure that all systems of the previous stage have completed before any
systems of the next stage begin, and that there is a moment in time when no
systems are in-progress.
This makes it possible/safe to apply Commands. Any operations
performed by systems using Commands are applied at the
end of that stage.
By default, when you add your systems, they are added to
CoreStage::Update. Startup systems are added to
StartupStage::Startup.
Bevy's internal systems are in the other stages, to ensure they are ordered
correctly relative to your game logic.
If you want to add your own systems to any of Bevy's internal stages, you
need to beware of potential unexpected interactions with Bevy's own internal
systems. Remember: Bevy's internals are implemented using ordinary systems
and ECS, just like your own stuff!
You can add your own additional stages. For example, if we want our debug
systems to run after our game logic:
fn main() {
    // label for our debug stage
    static DEBUG: &str = "debug";

    App::new()
        .add_plugins(DefaultPlugins)

        // add DEBUG stage after Bevy's Update
        // also make it single-threaded
        .add_stage_after(CoreStage::Update, DEBUG, SystemStage::single_threaded())

        // systems are added to the `CoreStage::Update` stage by default
        .add_system(player_gather_xp)
        .add_system(player_take_damage)

        // add our debug systems
        .add_system_to_stage(DEBUG, debug_player_hp)
        .add_system_to_stage(DEBUG, debug_stats_change)
        .add_system_to_stage(DEBUG, debug_new_hostiles)

        .run();
}
If you need to manage when your systems run, relative to one another, it
is generally preferable to avoid using stages, and to use explicit system
ordering instead. Stages limit parallel execution and
the performance of your game.
However, stages can make it easier to organize things, when you really want
to be sure that all previous systems have completed. Stages are also the
only way to apply Commands.
If you have systems that need to rely on the actions that other systems have
performed by using Commands, and need to do so during the
same frame, placing those systems into separate stages is the only way to
accomplish that.

### References
[[Systems  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] 