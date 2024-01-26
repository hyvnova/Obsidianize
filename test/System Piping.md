Bevy Version:0.9(outdated!)


System Piping
Relevant official examples:
system_piping.

You can compose a single Bevy system from multiple Rust functions.
You can make functions that can take an input and produce an output, and be
connected together to run as a single larger system. This is called "system piping".
You can think of it as creating "modular" systems made up of multiple building
blocks. This way, you can reuse some common code/logic in multiple systems.
Note that system piping is not a way of communicating between systems.
If you want to pass data between systems, you should use Events
instead.
Example: Handling Results
One useful application of system piping is to be able to return errors (allowing
the use of Rust's ? operator) and then have a separate function for handling
them:
fn net_receive(mut netcode: ResMut<MyNetProto>) -> std::io::Result<()> {
    netcode.receive_updates()?;

    Ok(())
}

fn handle_io_errors(In(result): In<std::io::Result<()>>) {
    if let Err(e) = result {
        eprintln!("I/O error occurred: {}", e);
    }
}
Such functions cannot be registered individually as systems (Bevy
doesn't know what to do with the input/output). By "piping" them together, we
create a valid system that we can add:
fn main() {
    App::new()
        // ...
        .add_system(net_receive.pipe(handle_io_errors))
        // ...
        .run();
}
Performance Warning
Beware that Bevy treats the whole chain as if it was a single big system, with
all the combined system parameters and their respective data access
requirements. This implies that parallelism could be limited, affecting
performance.
If you create multiple "piped systems" that all contain a common function which
contains any mutable access, that prevents all of them from running in parallel!

### References
[[Systems  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] 