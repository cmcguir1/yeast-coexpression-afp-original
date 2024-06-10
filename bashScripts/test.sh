#ssh cmcguir1@janus02.cs.trinity.edu "touch test_shh.txt"

if ssh -qn cmcguir1@janus02.cs.trinity.edu pidof httpd &>/dev/null ; then
     echo "Janus02 is running";
     exit 0;
else
     echo "Janus02 is not running";
     exit 1;
fi