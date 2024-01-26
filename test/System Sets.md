Bevy Version:0.9(outdated!)


System Sets
System Sets allow you to easily apply common properties to multiple systems,
for purposes such as labeling, ordering,
run criteria, and states.
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)

        // group our input handling systems into a set
        .add_system_set(
            SystemSet::new()
                .label("input")
                .with_system(keyboard_input)
                .with_system(gamepad_input)
        )

        // our "net" systems should run before "input"
        .add_system_set(
            SystemSet::new()
                .label("net")
                .before("input")
                // individual systems can still have
                // their own labels (and ordering)
                .with_system(server_session.label("session"))
                .with_system(server_updates.after("session"))
        )

        // some ungrouped systems
        .add_system(player_movement.after("input"))
        .add_system(session_ui.after("session"))
        .add_system(smoke_particles)

        .run();
}

### References
[[System Order of Execution  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[The page been moved to httpsbevycheatbookgithubioprogrammingsystemsetshtml]] 