#!/usr/bin/env python3

import pybullet as p
import time

physicsClient = p.connect(p.GUI)

for i in range (0,1000):
	p.stepSimulation()
	time.sleep(1/60)
p.disconnect()
