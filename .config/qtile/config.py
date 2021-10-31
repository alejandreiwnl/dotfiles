import os
import re
import socket
import subprocess
from libqtile import qtile, bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from colors import gruvbox

alt = "mod1"
mod = "mod4"
terminal = "alacritty"
browser = "brave"
officesuite = "libreoffice"

keys = [
    # restart qtile
    Key([mod, "shift"], "r",
        lazy.restart(),
        desc = "Restarts Qtile"
        ),

    # spawn programs
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc = "Launches default terminal"
        ),
    Key([mod, "shift"], "Return",
        lazy.spawn("rofi -show drun -theme ~/.config/rofi/launcher.rasi"),
        desc = "Runs launcher with specified theme"
        ),
    Key([], "Print",
        lazy.spawn("flameshot gui"),
        desc = "Runs screenshot tool"
        ),
    KeyChord(["control"], "x",[
        Key([], "b",
            lazy.spawn(browser),
            desc = "Launches default browser"
            ),
        Key([], "s",
            lazy.spawn("slack"),
            desc = "Launches Slack"
            ),
        Key([], "o",
            lazy.spawn(officesuite),
            desc = "Launches default Office Suite"
            ),
        ]),

    # change window focus
    Key([mod], "j",
        lazy.layout.down(),
        desc = "Switch window focus down"
        ),
    Key([mod], "k",
        lazy.layout.up(),
        desc = "Switch window focus up"
        ),
    Key([mod], "h", 
        lazy.layout.left(),
        desc = "Switch window focus left"
        ),
    Key([mod], "l",
        lazy.layout.right(),
        desc = "Switch window focus right"
        ),

    # shuffle/swap windows
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc = "Move focused window down"
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc = "Move focused window up"
        ),
    Key([mod, "shift"], "h",
        lazy.layout.swap_left(),
        lazy.layout.shuffle_left(),
        desc = "Move focused window to the left"
        ),
    Key([mod, "shift"], "l",
        lazy.layout.swap_right(),
        lazy.layout.shuffle_right(),
        desc = "Move focused window to the right"
        ),

    # manupilate window size
    Key([alt], "j",
        lazy.layout.grow_down().when(layout = 'columns'),
        desc = "Increases window size down when using columns layout"
        ),
    Key([alt], "k",
        lazy.layout.grow_up().when(layout = 'columns'),
        desc = "Increases window size up when using columns layout"
        ),
    Key([alt], "h",
        lazy.layout.grow_left().when(layout = 'columns'),
        lazy.layout.shrink().when(layout = 'monadtall'),
        desc = "Increases window size to the left when using columns layout/Decreases space when using monadtall layout"
        ),
    Key([alt], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        desc = "Increases window size to the right when using columns layout/Increase space when using monadtall layout"
        ),
    
    # other window controls
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc = "Fullscreen toggle"
        ),
    Key([mod], "Escape",
        lazy.window.kill(),
        desc = "Kills focused window"
        ),

    # other layout controls
    Key([mod], "Tab",
        lazy.next_layout(),
        desc = "Cycle through enabled layouts"
        ),
    Key([mod], "q",
        lazy.layout.flip().when(layout = 'monadtall'),
        lazy.layout.swap_column_left().when(layout = 'columns'),
        desc = "Flips window panes"
        ),
    Key([mod], "s",
        lazy.layout.toggle_split().when(layout = 'columns'),
        desc = "Split mode/Stack mode toggle"
        ),
    Key([alt], "n",
        lazy.layout.normalize(),
        desc = "Normalizes window size ratios. Excludes master pane when using monadtall layout" 
        ),
    Key([alt, "shift"], "n",
        lazy.layout.reset(),
        desc = "Normalizes window size ratios including the master pane when using  monadtall layout"
        ),
    Key([alt], "m",
        lazy.layout.maximize(),
        desc = "Maximizes focused window"
        ),
    ]

group_names = [("1", {'layout': 'monadtall'}),
               ("2", {'layout': 'monadtall'}),
               ("3", {'layout': 'columns'}),
               ("4", {'layout': 'columns'}),
               ("5", {'layout': 'stack'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name,kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen())) #switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) #send current window to specified group

layout_theme = {
    "border_width": 2,
    "margin": 5,
    "border_focus": gruvbox['chamois'],
    "border_normal": gruvbox['masala']
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Columns(
        **layout_theme,
        border_focus_stack = gruvbox['yellow'],
        border_normal_stack = gruvbox['masala'],
        border_on_single = True),
    layout.Stack(
        **layout_theme,
        num_stacks = 1),
    #layout.MonadWide(),
    #layout.RatioTile(),
    #layout.Floating(),
    #layout.Bsp(),
    #layout.Matrix(),
    #layout.Max,
    #layout.Slice(),
    #layout.Tile(),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy()
]

widget_defaults = dict(
    font = "Noto Sans",
    fontsize = 14,
    padding = 2,
    foreground = gruvbox['chamois'],
    background = gruvbox['mine-shaft'],
)

extenstion_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
            widget.Spacer(
                length = 10
                ),
            widget.GroupBox(
                active = gruvbox['chamois'],
                inactive = gruvbox['masala'],
                highlight_method = "line",
                highlight_color = gruvbox['dune'],
                this_current_screen_border = gruvbox['chamois'],
                spacing = 5,
                use_mouse_wheel = False,
                disable_drag = True
                ),
            widget.Spacer(
                length = 15
                ),
            widget.CurrentLayout(
                foreground = gruvbox['yellow']
                ),
            widget.Sep(
                padding = 10,
                size_percent = 30,
                linewidth = 2,
                foreground = gruvbox['aqua']
                ),
            widget.WindowName(
                max_chars = 40
                ),
            widget.Clock(
                format='%a,%Y-%m-%d'
                ),
            widget.Sep(
                padding = 10,
                size_percent = 50,
                linewidth = 2,
                foreground = gruvbox['aqua']
                ),
            widget.Clock(
                format='%H:%M'
                ),
            widget.Spacer(),
            widget.Systray(),
            widget.Sep(
                padding = 10,
                size_percent = 30,
                linewidth = 2,
                foreground = gruvbox['aqua']
                ),
            widget.PulseVolume(
                step = 2,
                fmt = 'Volume: {}'
                ),
            widget.Sep(
                padding = 10,
                size_percent = 30,
                linewidth = 2,
                foreground = gruvbox['aqua']
                ),
            widget.CheckUpdates(
                colour_have_updates = gruvbox['chamois'],
                colour_no_updates = gruvbox['masala'],
                update_interval = 3600,
                distro = "Arch_checkupdates", #uses 'checkupdates' from pacman-contrib
                display_format= "Updates: {updates}",
                no_update_string = "0 Updates",
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --hold -e checkupdates')}
                ),
            widget.Sep(
                padding = 10,
                size_percent = 30,
                linewidth = 2,
                foreground = gruvbox['aqua']
                ),
            widget.ThermalSensor(
                fmt = 'CPU: {}',
                tag_sensor = "Tdie",
                foreground = gruvbox['chamois'],
                update_interval = 3
                ),
            widget.NvidiaSensors(
                foreground = gruvbox['chamois'],
                update_interval = 3,
                format = 'GPU: {temp}°C'
                ),
            widget.Sep(
                padding = 10,
                size_percent = 30,
                linewidth = 2,
                foreground = gruvbox['aqua']
                ),
            widget.CPUGraph(
                border_color = gruvbox['mine-shaft'],
                graph_color = gruvbox['purple'],
                fill_color = gruvbox['purple'],
                line_width = 2 
                ),
            widget.Sep(
                padding = 10,
                size_percent = 30,
                linewidth = 2,
                foreground = gruvbox['aqua']
                ),
            widget.NetGraph(
                border_color = gruvbox['mine-shaft'],
                graph_color = gruvbox['blue'],
                fill_color = gruvbox['blue'],
                line_width = 2
                ),
            widget.Sep(
                padding = 10,
                size_percent = 30,
                linewidth = 2, 
                foreground = gruvbox['aqua']
                ),
            widget.MemoryGraph(
                border_color = gruvbox['mine-shaft'],
                graph_color = gruvbox['orange'],
                fill_color = gruvbox['orange'],
                line_width = 2
                ),
            widget.Spacer(
                length = 10
                )
        ]
    return widgets_list

# screens/bar
def init_screens():
    return [Screen(top = bar.Bar(widgets = init_widgets_list(), size = 30, margin = [5, 10, 0, 10]))]

screens = init_screens()

# drag floating layouts
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start = lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start = lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

floating_layout = layout.Floating(
    border_width = 2,
    border_focus = gruvbox['yellow'],
    border_normal = gruvbox['masala'],
    float_rules = [
            #run the utility of `xprop` to see the wm class and name of an X client.
            *layout.Floating.default_float_rules,
            Match(wm_class = 'confirmreset'),  #gitk
            Match(wm_class = 'makebranch'),  #gitk
            Match(wm_class = 'maketag'),  #gitk
            Match(wm_class = 'ssh-askpass'),  #ssh-askpass
            Match(title = 'branchdialog'),  #gitk
            Match(title = 'pinentry'),  #GPG key password entry
    ]
)

dgroups_key_binder = None
dgroups_app_rules = []  #type: List
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wmname = "Qtile"
