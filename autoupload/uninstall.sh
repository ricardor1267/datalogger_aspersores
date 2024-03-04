systemctl stop autoupload
systemctl disable autoupload
rm /etc/systemd/system/autoupload.service
systemctl daemon-reload

