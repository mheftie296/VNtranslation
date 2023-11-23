# VNtranslation
Attempted machine translation of the Nintendo Switch version of the game "Let's spend the future together [Jinrui no Minasama e]" using ALMA ja V2 and the koboldCPP api.
This currently causes the game to crash when the patch is applied and too much text has been translated.
I suspect it is translating important internal game text but I am having trouble figuring out the encoding.

Running this script requires extracting one of the AKBG_Chapter**.book files from resources.assets in the game files, it is currently hardcoded for Chapter 1.
