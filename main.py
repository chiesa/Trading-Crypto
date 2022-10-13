#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
from materiale_utile.gestione_main import gestione
g = gestione()

while True:
	ret = g.gestione_main()
	if ret == "fine":
		break
