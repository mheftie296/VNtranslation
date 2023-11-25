# VNtranslation
Attempted machine translation of the Nintendo Switch version of the game "Let's spend the future together [Jinrui no Minasama e]" using ALMA ja V2 and the koboldCPP api.
The script attempts to find the correct strings to translate using the hex byte before the string, the game has stopped crashing

Running this script requires extracting and replacing one of the AKBG_Chapter**.book files from resources.assets in the game files, it is currently hardcoded for Chapter 1.

Current issues:

-Too long translations are currently replaced with 'TL'

-Only the Visual Novel sections are translated

-The translations are bad

I was hoping the LLM would let me use the previous lines as context but that might not be an option