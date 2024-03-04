for service in autoupload  server serialRead
do
    cd $service
    sh install.sh
    cd ..
done

cd /srv/datalogger_aspersores/
systemctl stop server
systemctl stop autoupload
mysql < /srv/datalogger_aspersores/install.sql
systemctl restart server
systemctl restart autoupload
