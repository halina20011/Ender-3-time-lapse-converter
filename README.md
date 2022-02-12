<h1>Work in progress</h1>

<div id="header" align="center">
    <img src="https://github.com/halina20011/halina20011/blob/main/Halina-Circle.png" width="100"/>
    <div id="badges">
        <a href="https://www.youtube.com/channel/UCG0h6r6T1joRASO29JV9qMQ">
            <img src="https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=youtube&logoColor=white" alt="Youtube Badge"/>
        </a>
        <a href="https://halina-website.firebaseapp.com/">
            <img src="https://img.shields.io/badge/Website-lightgrey?style=for-the-badge" alt="Website"/>
        </a>
        <a href="https://www.instagram.com/mario.durakovic/">
            <img src="https://img.shields.io/badge/Instagram-blue?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram Badge"/>
        </a>
    </div>
</div>

<h2>How to change some program settings?</h2>

<p>In working directory, there is file with name ''settings.json" (/settings.json). In there there are values you can change. </p>

setting | info | type
--- | --- | ---
| ```GCodeTriggerPosition``` | This value controls where to move printer head to take photo. Don't set z axis and speed in it! Speed you change in "speed" setting. | string |
| ```speed``` | Change speed. | string
 ```runCommandWhenTakingPicture``` | Add additional gcode to run. | list |
| ```retraction``` | How much retraction need printer do before and after taking photo in mm. | negative float |
 ```showLayerNumber``` | if this variable is set to true: the screen will show the current printing layer. | boolean
| ```waitTime``` | How much seconds to wait, after printer head arrive to ```GCodeTriggerPosition``` | int

<h2>How to run file?</h2>
<p>You can run file with arguments:</p>

```
python main.py [Original file] [Path where to store generated file]
```
<p>Or you can run file without arguments and that will program ask for them:</p>