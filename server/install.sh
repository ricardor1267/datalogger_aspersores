systemctl stop server
systemctl disable server
rm /etc/systemd/system/server.service
systemctl daemon-reload
cp /srv/datalogger_aspersores/server/server.service /etc/systemd/system/server.service
systemctl enable server
systemctl restart server