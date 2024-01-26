Bevy Version:0.12(current)


Non-Send Resources
"Non-send" refers to data types that must only be accessed from the "main
thread" of the application. Such data is marked by Rust as !Send (lacking
the Send trait).
Some (often system) libraries have interfaces that cannot be safely used from
other threads. A common example of this are various low-level OS interfaces
for things like windowing, graphics, or audio. If you are doing advanced
things like creating a Bevy plugin for interfacing with such things, you
may encounter the need for this.
Normally, Bevy works by running all your systems on a
thread-pool, making use of many CPU cores. However, you might need to ensure
that some code always runs on the "main thread", or access data that is not
safe to access in a multithreaded way.
Non-Send Systems and Data Access
To do this, you can use a NonSend<T> /
NonSendMut<T> system parameter. This behaves just like
Res<T> / ResMut<T>, letting you access an
ECS resource (single global instance of some data), except that
the presence of such a parameter forces the Bevy scheduler to always run the
system on the main thread. This ensures that data never has
to be sent between threads or accessed from different threads.
One example of such a resource is WinitWindows in Bevy.
This is the low-level layer behind the window entities that you
typically use for window management. It gives you more direct access to OS
window management functionality.
fn setup_raw_window(
    q_primary: Query<Entity, With<PrimaryWindow>>,
    mut windows: NonSend<WinitWindows>
) {
    let raw_window = windows.get_window(q_primary.single());
    // do some special things using `winit` APIs
}
// just add it as a normal system;
// Bevy will notice the NonSend parameter
// and ensure it runs on the main thread
app.add_systems(Startup, setup_raw_window);
Custom Non-Send Resources
Normally, to insert resources, their types must be
Send.
Bevy tracks non-Send resources separately, to ensure that they
can only be accessed using NonSend<T> /
NonSendMut<T>.
It is not possible to insert non-send resources using
Commands, only using direct World access.
This means that you have to initialize them in an exclusive
system, FromWorld impl,
or custom stage.
fn setup_platform_audio(world: &mut World) {
    // assuming `OSAudioMagic` is some primitive that is not thread-safe
    let instance = OSAudioMagic::init();

    world.insert_non_send_resource(instance);
}
app.add_systems(Startup, setup_platform_audio);

### References
[[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Exclusive Systems  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Window Properties  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 