#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from kivy.config import Config
#Config.set("graphics", "fullscreen", "auto")
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window, Keyboard


vanster = Keyboard.string_to_keycode(None, "left")
hoger = Keyboard.string_to_keycode(None, "right")


def flytta_pos(sak, sidled, hojdled):
    ny_x = sak.pos[0] + sidled
    ny_y = sak.pos[1] + hojdled
    sak.pos = ny_x, ny_y


class Sak(Widget):
    def __init__(self, plats, storlek):
        Widget.__init__(self)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.pos = plats
        self.size = storlek

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Bil(Sak):
    def flytta(self, knappar):
        for knapp in knappar:
            if knapp == vanster:
                flytta_pos(self, -3, 0)
                break
            if knapp == hoger:
                flytta_pos(self, 3, 0)
                break


class Hinder(Sak):
    def flytta(self, knappar):
        flytta_pos(self, 0, -3)


class Bilspel(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.knappar = list()

        Window.bind(on_key_down=self.knapp_ner, on_key_up=self.knapp_upp)

        self.bil = Bil(plats=(400, 0), storlek=(50, 100))
        self.add_widget(self.bil)
        self.hinder = Hinder(plats=(400, 600), storlek=(100, 100))
        self.add_widget(self.hinder)

    def flytta(self, tid):
        for sak in self.children:
            sak.flytta(self.knappar)

        if self.bil.collide_widget(self.hinder):
            self.remove_widget(self.bil)

    def knapp_ner(self, window, knapp, knappkod, text, modifierare):
        if knapp not in self.knappar:
            self.knappar.insert(0, knapp)

    def knapp_upp(self, window, knapp, knappkod):
        if knapp in self.knappar:
            self.knappar.remove(knapp)


class Spelet(App):
    def build(self):
        spel = Bilspel()
        Clock.schedule_interval(spel.flytta, 1.0/60.0)
        return spel


if __name__ == '__main__':
    Spelet().run()
