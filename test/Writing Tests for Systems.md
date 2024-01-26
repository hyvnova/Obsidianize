Bevy Version:0.9(outdated!)


Writing Tests for Systems
You might want to write and run automated tests for your systems.
You can use the regular Rust testing features (cargo test) with Bevy.
To do this, you can create an empty ECS World in your
tests, and then, using direct World access, insert whatever
entities and resources you need for testing. Create
a standalone stage with the systems you want to
run, and manually run it on the World.
Bevy's official repository has a fantastic example of how to do
this.

### References
[[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 