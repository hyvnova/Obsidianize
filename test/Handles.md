Bevy Version:0.9(outdated!)


Handles
Handles are lightweight IDs that refer to a specific asset. You need them
to use your assets, for example to spawn entities like
2D sprites or 3D models, or to access the data
of the assets.
Handles have the Rust type Handle<T>, where T is the
asset type.
You can store handles in your entity components or
resources.
Handles can refer to not-yet-loaded assets, meaning you can just spawn your
entities anyway, using the handles, and the assets will just "pop in" when
they become ready.
Obtaining Handles
If you are loading an asset from a file, the
asset_server.load(…) call will give you the handle. The loading of the
data happens in the background, meaning that the handle will initially refer
to an unavailable asset, and the actual data will become available later.
If you are creating your own asset data from code,
the assets.add(…) call will give you the handle.
Reference Counting; Strong and Weak Handles
Bevy keeps track of how many handles to a given asset exist at any time. Bevy
will automatically unload unused assets, after the last handle is dropped.
For this reason, creating additional handles to the same asset requires you
to call handle.clone(). This makes the operation explicit, to ensure you are
aware of all the places in your code where you create additional handles. The
.clone() operation is cheap, so don't worry about performance (in most cases).
There are two kinds of handles: "strong" and "weak". Strong assets are
counted, weak handles are not. By default, handles are strong. If you want
to create a weak handle, use .clone_weak() (instead of .clone()) on an
existing handle. Bevy can unload the asset after all strong handles are gone,
even if you are still holding some weak handles.
Untyped Handles
Bevy also has a HandleUntyped type. Use this type
of handle if you need to be able to refer to any asset, regardless of the
asset type.
This allows you to store a collection (such as Vec or
HashMap) containing assets of mixed types.
You can create an untyped handle using .clone_untyped() on an existing
handle.
Just like regular handles, untyped handles can be strong or weak.
You need to do this to access the asset data.
You can convert an untyped handle into a typed handle with .typed::<T>(),
specifying the type to use. You need to do this to access the asset
data.

### References
[[3D Models and Scenes GLTF  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Sprites and Atlases  Unofficial Bevy Cheat Book]] [[Load Assets from Files  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Access the Asset Data  Unofficial Bevy Cheat Book]] 