Bevy Version:0.11(outdated!)


Dev Tools and Editors for Bevy
Bevy does not yet have an official editor or other such tools. An official
editor is planned as a long-term future goal. In the meantime, here are
some community-made tools to help you.

Editor
bevy_inspector_egui gives you a simple
editor-like property inspector window in-game. It lets you modify the values of
your components and resources in real-time as the game is running.
bevy_editor_pls is an editor-like interface that
you can embed into your game. It has even more features, like switching app
states, fly camera, performance diagnostics, and inspector panels.
space_editor is another such editor that can be
embedded into your game. It seems to be designed for a Unity-inspired prefab
workflow.
You can also use Blender as a level/scene editor,
by exporting your scenes to GLTF. The Blender Bevy Components
Workflow project improves on this
experience, by allowing you to setup your Bevy ECS Components
in Blender, include them in the exported GLTF, and use them in Bevy.
Diagnostics
bevy_mod_debugdump is a tool to help visualize
your App Schedules (all of the registered
systems with their ordering
dependencies), and the Bevy Render Graph.

### References
[[3D Models and Scenes GLTF  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] 