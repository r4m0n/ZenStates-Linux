#!/usr/bin/python3
import portio

portio.iopl(3)
portio.ioperm(0x2E, 2, 1)

portio.outb_p(0x87, 0x2E)
portio.outb_p(0x01, 0x2E)
portio.outb_p(0x55, 0x2E)
portio.outb_p(0x55, 0x2E)
portio.outb_p(0x07, 0x2E)
portio.outb_p(0x03, 0x2F)
portio.outb_p(0xF0, 0x2E)
f = portio.inb_p(0x2F)
f ^= 0x08
portio.outb_p(f, 0x2F)
