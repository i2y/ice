import ice.core.builtins

if isinstance(__builtins__, dict) {
    __builtins__.update(ice.core.builtins.global_env)
}
else {
    __builtins__.__dict__.update(ice.core.builtins.global_env)
}