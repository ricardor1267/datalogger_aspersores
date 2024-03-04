systemctl stop server
systemctl disable server
rm /etc/systemd/system/server.service
systemctl daemon-reload
