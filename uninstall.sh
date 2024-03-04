for service in autoupload  server serialRead
do
    cd $service
    sh uninstall.sh
    cd ..
done

