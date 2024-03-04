systemctl stop autoupload
systemctl disable autoupload
rm /etc/systemd/system/autoupload.service
systemctl daemon-reload
cp /srv/datalogger_aspersores/autoupload/autoupload.service /etc/systemd/system/autoupload.service
systemctl enable autoupload
systemctl restart autoupload
