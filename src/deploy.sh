vr_val=$1
echo $vr_val
v1 = "dwsduscaahuimage"
v3="dwsduscaahuimage:v$v2"
if [ $vr_val =="" ]
then
   echo "Enter Image Version Number."
   sudo docker images | awk '$1 ~ /dwsduscaahuimage/ { print $2, $1, $2, $4, $5, $6, $7}'
   echo "----------------------------Deployment Start-----------------------------"
   echo "Enter TAG version"
   read v2
   v3="dwsduscaahuimage:v$v2"
   echo "-------- new Tag -----"
   echo "dwsduscahuconreg.azurecr.io/$v3"
   echo "----------------------"
   echo "Do you want to continue(0 for no)"
   read flag
   if [ $flag -gt 0 ]
   then
	echo "sudo sudo docker build --tag dwsduscaahuimage ."
	sudo sudo docker build --tag dwsduscaahuimage .

	echo "sudo sudo docker tag dwsduscaahuimage dwsduscahuconreg.azurecr.io/$v3"
	sudo sudo docker tag dwsduscaahuimage dwsduscahuconreg.azurecr.io/$v3

	echo "az webapp config container set --name dws-d-usc-ahu-cnn-02-svc --resource-group dws-d-usc-ahu-rg --docker-custom-image-name dwsduscahuconreg.azurecr.io/$v3 --docker-registry-server-url https://dwsduscahuconreg.azurecr.io --docker-registry-server-user dwsduscahuconreg --docker-registry-server-password HATvJL5Zu9Swuj5GtnOV83en/eNjOB3B"
	az webapp config container set --name dws-d-usc-ahu-cnn-02-svc --resource-group dws-d-usc-ahu-rg --docker-custom-image-name dwsduscahuconreg.azurecr.io/$v3 --docker-registry-server-url https://dwsduscahuconreg.azurecr.io --docker-registry-server-user dwsduscahuconreg --docker-registry-server-password HATvJL5Zu9Swuj5GtnOV83en/eNjOB3B

	echo "sudo docker push dwsduscahuconreg.azurecr.io/$v3"
	sudo docker push dwsduscahuconreg.azurecr.io/$v3

	echo "az acr repository list -n dwsduscahuconreg"
	az acr repository list -n dwsduscahuconreg

	echo "az webapp config appsettings set --resource-group dws-d-usc-ahu-rg --name dws-d-usc-ahu-cnn-02-svc --settings WEBSITES_PORT=8000"
	az webapp config appsettings set --resource-group dws-d-usc-ahu-rg --name dws-d-usc-ahu-cnn-02-svc --settings WEBSITES_PORT=8000

	echo "az webapp restart --name dws-d-usc-ahu-cnn-02-svc --resource-group dws-d-usc-ahu-rg"
	az webapp restart --name dws-d-usc-ahu-cnn-02-svc --resource-group dws-d-usc-ahu-rg

	echo "---------------------------- Deployed Successfully --------"
	echo ""
   else
        echo "------------------ Deployment Exited ----------------------"	  
        echo ""	
   fi
else
   echo "------------------ Exit ---------------------"
   echo ""
fi

