import pygame

from src.Data.InputDataFile import InputDataFile
from src.Data.InputDataStub import InputDataStub
from src.Display.ConsoleOutputs import *
from src.Display.IOLogger import IOLogger

pygame.mixer.init()


def playSound(filePath, currentMusic, directoryPath, logger, volume):
    pygame.mixer.stop()
    pygame.mixer.init()
    soundPlayer = pygame.mixer.Sound(directoryPath + "/" + filePath)
    pygame.mixer.Sound.set_volume(soundPlayer, volume)
    soundPlayer.play()
    logger.ShowOutput("Now playing:" + filePath)

    return soundPlayer


def stopSound(soundPlayer, logger):
    if pygame.mixer.get_busy():
        soundPlayer.stop()
        logger.ShowOutput("Song stopped.")
    else:
        logger.ShowOutput("There is no song playing at the moment")


def getPlaylist(inputType, directoryPath):
    playlist = inputType.getRawData(directoryPath)
    return playlist


def getFileToPlay(fileList, logger):
    displayFiles(fileList, logger)

    fileIdentifier = logger.TakeInput("Please enter the track number:")
    while int(fileIdentifier) not in range(len(fileList)):
        logger.ShowOutput("This is an invalid track number.")
        fileIdentifier = logger.TakeInput("Please enter the track number:")

    if int(fileIdentifier) in range(len(fileList)):
        fileIdentifier = fileList[int(fileIdentifier)]

    return fileIdentifier


def InitialiseLogs():
    with open("Logs/InputLog.txt", "w") as inputs:
        inputs.write("")
    with open("Logs/OutputLog.txt", "w") as outputs:
        outputs.write("")


def enterCommand(soundPlayer, songList, directoryPath, optionsList, volume, logger=IOLogger()):
    print(optionsList)
    command = logger.TakeInput("Please type one of the options").lower()

    if command == "stop":
        stopSound(soundPlayer, logger)

    elif command == "play":

        songName = getFileToPlay(songList, logger)
        soundPlayer = playSound(songName, soundPlayer, directoryPath, logger, volume)

    elif command == "volume":
        volume = float(input("What would you like the volume to be between 0 for mute and 10?"))
        volume = volume/10

    else:
        logger.ShowOutput("That is not a valid command")

    return soundPlayer, volume


def main():
    soundPlayer = ""
    directoryPath = "Music"
    optionsList = ["Play", "Stop", "Volume"]
    volume = 1.0
    InitialiseLogs()
    musicFiles = getPlaylist(InputDataFile(), directoryPath)
    while True:
        soundPlayer, volume = enterCommand(soundPlayer, musicFiles, directoryPath, optionsList, volume)


if __name__ == '__main__':
    main()
