systemctl stop serialRead
systemctl disable serialRead
rm /etc/systemd/system/serialRead.service
systemctl daemon-reload
cp /srv/datalogger_aspersores/serialRead/serialRead.service /etc/systemd/system/serialRead.service
systemctl enable serialRead
systemctl restart serialRead
