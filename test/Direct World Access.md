Bevy Version:0.9(outdated!)


Direct World Access
The World is where Bevy ECS stores all data and
associated metadata. It keeps track of resources, entities and
components.
Typically, the App's schedule runner will run all
stages (which, in turn, run their systems)
on the main world. Regular systems are limited in
what data they can access from the world, by their system parameter
types. Operations that manipulate the world itself
are only done indirectly using Commands. This is how most
typical Bevy user code behaves.
However, there are also ways you can get full direct access to the world,
which gives you full control and freedom to do anything with any data stored
in the Bevy ECS:

Exclusive systems
FromWorld impls
Via the App builder
Manually created Worlds for purposes like tests or scenes
Custom Commands
Custom Stage impls (not recommended, prefer exclusive systems)

Direct world access lets you do things like:

Freely spawn/despawn entities, insert/remove resources, etc., taking effect immediately
(no delay like when using Commands from a regular system)
Access any component, entities, and resources you want
Manually run arbitrary systems or stages

This is especially useful if you want to do things that do not fit within
Bevy's typical execution model/flow of just running systems once every frame
(organized with stages and labels).
With direct world access, you can implement custom control flow, like
looping some systems multiple times, selecting different systems to run in
different circumstances, exporting/importing data from files like scenes or
game saves, …
Working with the World
Here are some ways that you can make use of the direct world access APIs.
SystemState
The easiest way to do things is using a SystemState.
This is a type that "imitates a system", behaving the same way as a
system with various parameters would. All the same behaviors
like queries, change detection, and
even Commands are available. You can use any system
params.
It also tracks any persistent state, used for things like change
detection or caching to improve performance. Therefore,
if you plan on reusing the same SystemState multiple
times, you should store it somewhere, rather than creating a new one every
time. Every time you call .get(world), it behaves like another "run"
of a system.
If you are using Commands, you can choose when you
want to apply them to the world. You need to manually call .apply(world)
on the SystemState, to apply them.
// TODO: write code example
Running a Stage
If you want to run some systems (a common use-case is
testing), the easiest way is to construct an impromptu
SystemStage (stages). This way you reuse
all the scheduling logic that Bevy normally does when running systems.
// TODO: write code example
Navigating by Metadata
The world contains a lot of metadata that allows navigating all the data
efficiently, such as information about all the stored components, entities,
archeypes.
// TODO: write code example

### References
[[Queries  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Change Detection  Unofficial Bevy Cheat Book]] [[Exclusive Systems  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Writing Tests for Systems  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 