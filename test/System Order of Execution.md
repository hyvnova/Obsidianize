Bevy Version:0.9(outdated!)


System Order of Execution
Bevy's scheduling algorithm is designed to deliver maximum performance
by running as many systems as possible in parallel across the available
CPU threads.
This is possible when the systems do not conflict over the data they need
to access. However, when a system needs to have mutable (exclusive) access
to a piece of data, other systems that need to access the same data cannot
be run at the same time. Bevy determines all of this information from the
system's function signature (the types of the parameters it takes).
In such situations, the order is nondeterministic by default. Bevy takes
no regard for when each system will run, and the order could even change
every frame!
Does it even matter?
In many cases, you don't need to worry about this.
However, sometimes you need to rely on specific systems to run in a particular
order. For example:

Maybe the logic you wrote in one of your systems needs any modifications
done to that data by another system to always happen first?
One system needs to receive events sent by another system.
You are using change detection.

In such situations, systems running in the wrong order typically causes
their behavior to be delayed until the next frame. In rare cases, depending
on your game logic, it may even result in more serious logic bugs!
It is up to you to decide if this is important.
With many things in typical games, such as juicy visual effects, it probably
doesn't matter if they get delayed by a frame. It might not be worthwhile
to bother with it. If you don't care, leaving the order ambiguous may also
result in better performance.
On the other hand, for things like handling the player input controls,
this would result in annoying lag, so you should probably fix it.
Explicit System Ordering
If a specific system must always run before or after some other systems,
you can add ordering constraints:
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)

        // order doesn't matter for these systems:
        .add_system(particle_effects)
        .add_system(npc_behaviors)
        .add_system(enemy_movement)

        .add_system(input_handling)

        .add_system(
            player_movement
                // `player_movement` must always run before `enemy_movement`
                .before(enemy_movement)
                // `player_movement` must always run after `input_handling`
                .after(input_handling)
        )
        .run();
}
.before/.after may be used as many times as you need on one system.
Labels
For more advanced use cases, you can use labels. Labels can
either be strings, or custom types (like enums) that derive SystemLabel.
This allows you to affect multiple systems at once, with the same constraints. 
You can place multiple labels on one system. You can also use the same label
on multiple systems.
Each label is a reference point that other systems can be ordered around.

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
#[derive(SystemLabel)]
enum MyLabel {
    /// everything that handles input
    Input,
    /// everything that updates player state
    Player,
    /// everything that moves things (works with transforms)
    Movement,
    /// systems that update the world map
    Map,
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)

        // use labels, because we want to have multiple affected systems
        .add_system(input_joystick.label(MyLabel::Input))
        .add_system(input_keyboard.label(MyLabel::Input))
        .add_system(input_touch.label(MyLabel::Input))

        .add_system(input_parameters.before(MyLabel::Input))

        .add_system(
            player_movement
                .before(MyLabel::Map)
                .after(MyLabel::Input)
                // we can have multiple labels on this system
                .label(MyLabel::Player)
                .label(MyLabel::Movement)
                // can also use loose strings as labels
                .label("player_movement")
        )

        // … and so on …

        .run();
}
When you have multiple systems with common labels or ordering, it may be
convenient to use system sets.
Circular Dependencies
If you have multiple systems mutually depending on each other, then it is
clearly impossible to resolve the situation completely like that.
You should try to redesign your game to avoid such situations, or just accept
the consequences. You can at least make it behave predictably, using explicit
ordering to specify the order you prefer.

### References
[[System Sets  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[Change Detection  Unofficial Bevy Cheat Book]] [[The page been moved to httpsbevycheatbookgithubioprogrammingsystemsetshtml]] 