#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randint
from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window, Keyboard
from kivy.graphics.context_instructions import Scale
from kivy.uix.label import Label


vanster = Keyboard.string_to_keycode(None, "left")
hoger = Keyboard.string_to_keycode(None, "right")
ner = Keyboard.string_to_keycode(None, "down")
upp = Keyboard.string_to_keycode(None, "up")

gron = Color(0,1,0)
vit =Color(1,1,1)


def flytta_pos(sak, sidled, hojdled):
    ny_x = sak.pos[0] + sidled
    ny_y = sak.pos[1] + hojdled
    sak.pos = ny_x, ny_y


class Sak(Widget):
    def __init__(self, plats, storlek, farg):
        Widget.__init__(self)
        with self.canvas:
            self.canvas.add(farg)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.pos = plats
        self.size = (storlek[0], storlek[1])

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Bil(Sak):
    def __init__(self, *args):
        Sak.__init__(self, *args)
        self.hastighet = 7

    def flytta(self, knappar):
        for knapp in knappar:
            if knapp == vanster:
                flytta_pos(self, -self.hastighet, 0)
            if knapp == hoger:
                flytta_pos(self, self.hastighet, 0)
            if knapp == upp:
                flytta_pos(self, 0, self.hastighet)
            if knapp == ner:
                flytta_pos(self, 0, -self.hastighet)

class Hinder(Sak):
    def __init__(self, *args):
        Sak.__init__(self, *args)
        self.hastighet = randint(-5,5)

    def flytta(self, knappar):
        flytta_pos(self, self.hastighet, -6)


class Bilspel(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.knappar = list()
        Window.bind(on_key_down=self.knapp_ner, on_key_up=self.knapp_upp)
        self.bind(size=self.rita)
        self.poeng = 0
        # Bredd räknas om varje gång skärmen ändras och vid start,
        # höjd är alltid 1000.
        self.bredd = -1.0
        self.hojd = 1000.0

    def rita(self, *args):
        self.canvas.clear()
        skalning = float(self.height) / self.hojd
        self.bredd = self.width / skalning
        with self.canvas:
            Scale(skalning)

        self.bil = Bil((500, 0), (50, 100), vit)
        self.add_widget(self.bil)
        self.nytthinder()
        self.info = Label(color=(1,1,1,1),
                          pos=(0, 950),
                          font_size=50,
                          halign="left")
        self.info.bind(texture_size=self.info.setter('size'))

        self.skriv_info()
        self.add_widget(self.info)

    def skriv_info(self):
        self.info.text = "Poäng %d" % self.poeng

    def nytthinder(self):
        start = randint(0, int(self.bredd))
        self.hinder = Hinder((start, 1000), (100, 100), gron)
        self.add_widget(self.hinder)

    def flytta(self, tid):
        for sak in self.children:
            try:
                sak.flytta(self.knappar)
            except:
                pass

        if self.bil.collide_widget(self.hinder):
            self.poeng += 1
            self.skriv_info()
            self.remove_widget(self.hinder)
            self.nytthinder()

        if not self.hinder.collide_widget(self):
            self.remove_widget(self.hinder)
            self.nytthinder()
            self.poeng -= 1
            self.skriv_info()

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
