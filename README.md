```
sudo mousepad /etc/xdg/lxsession/LXDE-pi/desktop.conf
```
line #2:
window_manager=mutter
to
window_manager=openbox

```
sudo apt-get install mpv feh
mkdir code
cd code
git clone https://github.com/acastles91/pablo .
cd pablo/archivos
cp -r * ~/.config
cd ..
sudo chmod +x kassel.py
```
