<h1>Work in progress</h1>

<div id="header" align="center">
    <img src="https://github.com/halina20011/halina20011/blob/main/Halina-Circle.png" width="100"/>
    <div id="badges">
    <a href="https://www.youtube.com/channel/UCG0h6r6T1joRASO29JV9qMQ">
        <img src="https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=youtube&logoColor=white" alt="Youtube Badge"/>
    </a>
    <a href="https://www.instagram.com/mario.durakovic/">
        <img src="https://img.shields.io/badge/Instagram-blue?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram Badge"/>
    </a>
    </div>

</div>

<h2>How to change some program settings?</h2>
in working directory, there is file with name ''settings.json" (/settings.json). In there there are values you can change.

setting | info
--- | ---
| ```GCodeTriggerPosition``` | This value controls where to move printer head to take photo. Don't set z axis and speed in it! Speed you change in "speed" setting. |
<!-- --- | --- -->
| ```speed``` | Change speed. |
<!-- --- | --- -->
 ```runCommandWhenTakingPicture``` | Add additional gcode to run.

<h2>How to run file?</h2>
<p>You can run file with arguments:</p>

```
python main.py [Original file] [Path where to store generated file]
```
<p>Or you can run file without arguments and that will program ask for them:</p>