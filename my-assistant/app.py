"""app.py: the assistant's control panel."""

import flet as ft
import memory
import theme


def main(page: ft.Page):
    page.title = "Arthur — Control Panel"
    page.bgcolor = theme.GREY_BG
    page.padding = 0
    page.fonts = {"Space Grotesk": "https://fonts.gstatic.com/s/spacegrotesk/v16/V8mDoQDjQSkFtoMM3T6r8E7mF71Q-gOoraIAEj7oUXskPMBBSSJLm2E.ttf"}
    page.window_width = 420
    page.window_height = 860

    data = memory.load()

    # ---------- reusable pieces ----------

    def save_and_refresh():
        memory.save(data)
        render()

    def stat_card(number, label, color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(str(number), size=22, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(label, size=10, color=theme.INK_SOFT),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
            bgcolor=theme.CARD,
            border_radius=theme.RADIUS_MD,
            padding=14,
            alignment=ft.alignment.center,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=14, color="#0A0A0C10"),
        )

    def section_header(title):
        return ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=theme.INK)

    # ---------- ALARMS ----------

    def add_alarm(e):
        new_id = memory.next_id(data["alarms"])
        data["alarms"].append(
            {"id": new_id, "time": time_field.value or "07:00",
             "label": label_field.value or "Alarm",
             "sound": sound_field.value or "sounds/default.mp3",
             "enabled": True}
        )
        time_field.value = ""
        label_field.value = ""
        sound_field.value = ""
        save_and_refresh()

    def delete_alarm(alarm_id):
        data["alarms"] = [a for a in data["alarms"] if a["id"] != alarm_id]
        save_and_refresh()

    def toggle_alarm(alarm_id, value):
        for a in data["alarms"]:
            if a["id"] == alarm_id:
                a["enabled"] = value
        save_and_refresh()

    time_field = ft.TextField(label="Time (HH:MM)", width=110, bgcolor=theme.CARD)
    label_field = ft.TextField(label="Label", width=110, bgcolor=theme.CARD)
    sound_field = ft.TextField(label="Sound file", width=140, bgcolor=theme.CARD)

    def alarm_row(a):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Switch(value=a["enabled"], active_color=theme.CYAN,
                              on_change=lambda e, aid=a["id"]: toggle_alarm(aid, e.control.value)),
                    ft.Column(
                        [
                            ft.Text(a["time"], size=18, weight=ft.FontWeight.BOLD, color=theme.INK),
                            ft.Text(f'{a["label"]} · {a["sound"].split("/")[-1]}', size=11, color=theme.INK_SOFT),
                        ],
                        spacing=0, expand=True,
                    ),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=theme.CORAL,
                                  on_click=lambda e, aid=a["id"]: delete_alarm(aid)),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
            border=ft.border.only(bottom=ft.BorderSide(1, theme.LINE)),
        )

    def alarms_view():
        return ft.Column(
            [
                section_header("Alarms"),
                theme.card_container(
                    ft.Column([alarm_row(a) for a in data["alarms"]] or
                              [ft.Text("No alarms yet.", color=theme.INK_SOFT)])
                ),
                ft.Container(height=10),
                theme.card_container(
                    ft.Column(
                        [
                            ft.Text("Add alarm", size=13, weight=ft.FontWeight.BOLD),
                            ft.Row([time_field, label_field]),
                            sound_field,
                            ft.ElevatedButton("Add", bgcolor=theme.CYAN, color=theme.BLACK_DEEP,
                                               on_click=add_alarm),
                        ],
                        spacing=10,
                    )
                ),
            ],
            spacing=12,
        )

    # ---------- REMINDERS ----------

    def add_reminder(e):
        new_id = memory.next_id(data["reminders"])
        data["reminders"].append(
            {"id": new_id, "time": rem_time_field.value or "18:00",
             "text": rem_text_field.value or "Reminder", "done": False}
        )
        rem_time_field.value = ""
        rem_text_field.value = ""
        save_and_refresh()

    def delete_reminder(rid):
        data["reminders"] = [r for r in data["reminders"] if r["id"] != rid]
        save_and_refresh()

    def toggle_reminder(rid, value):
        for r in data["reminders"]:
            if r["id"] == rid:
                r["done"] = value
        save_and_refresh()

    rem_time_field = ft.TextField(label="Time (HH:MM)", width=110, bgcolor=theme.CARD)
    rem_text_field = ft.TextField(label="Reminder text", width=180, bgcolor=theme.CARD)

    def reminder_row(r):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Checkbox(value=r["done"], active_color=theme.CYAN,
                                on_change=lambda e, rid=r["id"]: toggle_reminder(rid, e.control.value)),
                    ft.Column(
                        [
                            ft.Text(r["text"], size=13, weight=ft.FontWeight.BOLD,
                                    color=theme.INK_SOFT if r["done"] else theme.INK),
                            ft.Text(r["time"], size=11, color=theme.INK_SOFT),
                        ],
                        spacing=0, expand=True,
                    ),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=theme.CORAL,
                                  on_click=lambda e, rid=r["id"]: delete_reminder(rid)),
                ]
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
            border=ft.border.only(bottom=ft.BorderSide(1, theme.LINE)),
        )

    def reminders_view():
        return ft.Column(
            [
                section_header("Reminders"),
                theme.card_container(
                    ft.Column([reminder_row(r) for r in data["reminders"]] or
                              [ft.Text("No reminders yet.", color=theme.INK_SOFT)])
                ),
                ft.Container(height=10),
                theme.card_container(
                    ft.Column(
                        [
                            ft.Text("Add reminder", size=13, weight=ft.FontWeight.BOLD),
                            ft.Row([rem_time_field, rem_text_field]),
                            ft.ElevatedButton("Add", bgcolor=theme.CYAN, color=theme.BLACK_DEEP,
                                               on_click=add_reminder),
                        ],
                        spacing=10,
                    )
                ),
            ],
            spacing=12,
        )

    # ---------- CONTACTS ----------

    def add_contact(e):
        if name_field.value:
            data["contacts"][name_field.value.lower()] = number_field.value or ""
            name_field.value = ""
            number_field.value = ""
            save_and_refresh()

    def delete_contact(name):
        data["contacts"].pop(name, None)
        save_and_refresh()

    name_field = ft.TextField(label="Name", width=140, bgcolor=theme.CARD)
    number_field = ft.TextField(label="Number", width=150, bgcolor=theme.CARD)

    def contact_row(name, number):
        return ft.Container(
            content=ft.Row(
                [
                    ft.CircleAvatar(content=ft.Text(name[0].upper()), bgcolor=theme.CYAN, color=theme.BLACK_DEEP),
                    ft.Column(
                        [
                            ft.Text(name.title(), size=13, weight=ft.FontWeight.BOLD, color=theme.INK),
                            ft.Text(number, size=11, color=theme.INK_SOFT),
                        ],
                        spacing=0, expand=True,
                    ),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=theme.CORAL,
                                  on_click=lambda e, n=name: delete_contact(n)),
                ]
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
            border=ft.border.only(bottom=ft.BorderSide(1, theme.LINE)),
        )

    def contacts_view():
        return ft.Column(
            [
                section_header("Contacts"),
                theme.card_container(
                    ft.Column([contact_row(n, num) for n, num in data["contacts"].items()] or
                              [ft.Text("No contacts yet.", color=theme.INK_SOFT)])
                ),
                ft.Container(height=10),
                theme.card_container(
                    ft.Column(
                        [
                            ft.Text("Add contact", size=13, weight=ft.FontWeight.BOLD),
                            ft.Row([name_field, number_field]),
                            ft.ElevatedButton("Add", bgcolor=theme.CYAN, color=theme.BLACK_DEEP,
                                               on_click=add_contact),
                        ],
                        spacing=10,
                    )
                ),
            ],
            spacing=12,
        )

    # ---------- PREFERENCES ----------

    def add_pref(e):
        if pref_key.value:
            data["preferences"][pref_key.value] = pref_value.value or ""
            pref_key.value = ""
            pref_value.value = ""
            save_and_refresh()

    def delete_pref(key):
        data["preferences"].pop(key, None)
        save_and_refresh()

    pref_key = ft.TextField(label="Key", width=140, bgcolor=theme.CARD)
    pref_value = ft.TextField(label="Value", width=150, bgcolor=theme.CARD)

    def pref_row(key, value):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(key, size=12, color=theme.INK_SOFT),
                            ft.Text(str(value), size=14, weight=ft.FontWeight.BOLD, color=theme.INK),
                        ],
                        spacing=0, expand=True,
                    ),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=theme.CORAL,
                                  on_click=lambda e, k=key: delete_pref(k)),
                ]
            ),
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
            border=ft.border.only(bottom=ft.BorderSide(1, theme.LINE)),
        )

    def preferences_view():
        return ft.Column(
            [
                section_header("Preferences"),
                theme.card_container(
                    ft.Column([pref_row(k, v) for k, v in data["preferences"].items()] or
                              [ft.Text("No preferences saved yet.", color=theme.INK_SOFT)])
                ),
                ft.Container(height=10),
                theme.card_container(
                    ft.Column(
                        [
                            ft.Text("Add preference", size=13, weight=ft.FontWeight.BOLD),
                            ft.Row([pref_key, pref_value]),
                            ft.ElevatedButton("Add", bgcolor=theme.CYAN, color=theme.BLACK_DEEP,
                                               on_click=add_pref),
                        ],
                        spacing=10,
                    )
                ),
            ],
            spacing=12,
        )

    # ---------- HOME ----------

    def home_view():
        next_alarm = data["alarms"][0]["time"] if data["alarms"] else "—"
        open_reminders = len([r for r in data["reminders"] if not r["done"]])
        return ft.Column(
            [
                ft.Row(
                    [
                        stat_card(len(data["alarms"]), "ALARMS", theme.CYAN),
                        stat_card(open_reminders, "REMINDERS", theme.AMBER),
                        stat_card(len(data["contacts"]), "CONTACTS", theme.GREEN_OK),
                    ],
                    spacing=10,
                ),
                ft.Container(height=6),
                theme.card_container(
                    ft.Column(
                        [
                            ft.Text("NEXT ALARM", size=10, color=theme.INK_SOFT),
                            ft.Text(next_alarm, size=32, weight=ft.FontWeight.BOLD, color=theme.INK),
                        ],
                        spacing=2,
                    )
                ),
            ],
            spacing=12,
        )

    # ---------- nav shell ----------

    body = ft.Container(padding=20, expand=True)

    def render():
        views = {
            "home": home_view,
            "alarms": alarms_view,
            "reminders": reminders_view,
            "contacts": contacts_view,
            "preferences": preferences_view,
        }
        body.content = ft.Column([views[nav.selected_index and list(views)[nav.selected_index] or "home"]()],
                                  scroll=ft.ScrollMode.AUTO)
        page.update()

    def on_nav_change(e):
        render()

    nav = ft.NavigationBar(
        selected_index=0,
        bgcolor=theme.CARD,
        indicator_color=theme.CYAN,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.ALARM_OUTLINED, selected_icon=ft.Icons.ALARM, label="Alarms"),
            ft.NavigationBarDestination(icon=ft.Icons.NOTIFICATIONS_OUTLINED, selected_icon=ft.Icons.NOTIFICATIONS, label="Reminders"),
            ft.NavigationBarDestination(icon=ft.Icons.PEOPLE_OUTLINE, selected_icon=ft.Icons.PEOPLE, label="Contacts"),
            ft.NavigationBarDestination(icon=ft.Icons.TUNE, selected_icon=ft.Icons.TUNE, label="Prefs"),
        ],
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.GRAPHIC_EQ, color=theme.BLACK_DEEP, size=18),
                            width=34, height=34, bgcolor=theme.CYAN, border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                        ft.Text("Arthur", size=17, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ],
                    spacing=10,
                ),
                ft.Text("Good day — here's what I'm tracking", size=12, color="#FFFFFF99"),
            ],
            spacing=6,
        ),
        gradient=theme.header_gradient(),
        padding=ft.padding.only(left=20, right=20, top=22, bottom=26),
    )

    page.add(
        ft.Column(
            [header, body, nav],
            spacing=0,
            expand=True,
        )
    )

    render()


ft.app(target=main)
