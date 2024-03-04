systemctl stop serialRead
systemctl disable serialRead
rm /etc/systemd/system/serialRead.service
systemctl daemon-reload

