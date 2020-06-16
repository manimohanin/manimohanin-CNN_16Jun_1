vr_val=$1
echo $vr_val
v1 = "dwsduscaimapge30apr1"
v3="dwsduscaimapge30apr1:v$v2"
if [ $vr_val =="" ]
then
   echo "Enter Image Version Number."
   sudo docker image ls | grep "dwsduscaimapge30apr1"
   echo "----------------------------Deployment Start-----------------------------"
   echo "Enter TAG version"
   read v2
   v3="dwsduscaimapge30apr1:v$v2"
   echo "-------- new Tag -----"
   echo "dwsduscahuacr30apr1.azurecr.io/$v3"
   echo "----------------------"
   echo "Do you want to continue(0 for no)"
   read flag
   if [ $flag -gt 0 ]
   then
	echo "sudo sudo docker build --tag dwsduscaimapge30apr1 ."
	sudo sudo docker build --tag dwsduscaimapge30apr1 .

	echo "sudo sudo docker tag dwsduscaimapge30apr1 dwsduscahuacr30apr1.azurecr.io/$v3"
	sudo sudo docker tag dwsduscaimapge30apr1 dwsduscahuacr30apr1.azurecr.io/$v3

	echo "az webapp config container set --name dws-d-usc-ahu-cnn-30apr1-svc --resource-group dws-d-usc-ahu-rg --docker-custom-image-name dwsduscahuacr30apr1.azurecr.io/$v3 --docker-registry-server-url https://dwsduscahuacr30apr1.azurecr.io --docker-registry-server-user dwsduscahuacr30apr1 --docker-registry-server-password 02n038z71fzzsU0=zrcg9cm5nWdKE1b/"
	az webapp config container set --name dws-d-usc-ahu-cnn-30apr1-svc --resource-group dws-d-usc-ahu-rg --docker-custom-image-name dwsduscahuacr30apr1.azurecr.io/$v3 --docker-registry-server-url https://dwsduscahuacr30apr1.azurecr.io --docker-registry-server-user dwsduscahuacr30apr1 --docker-registry-server-password 02n038z71fzzsU0=zrcg9cm5nWdKE1b/

	echo "sudo docker push dwsduscahuacr30apr1.azurecr.io/$v3"
	sudo docker push dwsduscahuacr30apr1.azurecr.io/$v3

	echo "az acr repository list -n dwsduscahuacr30apr1"
	az acr repository list -n dwsduscahuacr30apr1

	echo "az webapp config appsettings set --resource-group dws-d-usc-ahu-rg --name dws-d-usc-ahu-cnn-30apr1-svc --settings WEBSITES_PORT=8000"
	az webapp config appsettings set --resource-group dws-d-usc-ahu-rg --name dws-d-usc-ahu-cnn-30apr1-svc --settings WEBSITES_PORT=8000

	echo "az webapp restart --name dws-d-usc-ahu-cnn-30apr1-svc --resource-group dws-d-usc-ahu-rg"
	az webapp restart --name dws-d-usc-ahu-cnn-30apr1-svc --resource-group dws-d-usc-ahu-rg

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

