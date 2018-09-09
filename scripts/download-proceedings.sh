for name in $(cat $1); do
  echo "=====  "$name"  ====="

  x=$(echo $name | cut -d\| -f1)
  url=$(echo $name | cut -d\| -f2)
  if test $x = $url; then
    url="https://www.softconf.com/emnlp2018/$x/manager/aclpub/proceedings.tgz"
  fi
  echo $x $url
  [[ ! -d "data/$x" ]] && mkdir -p data/$x
  cd data/$x
  wget -N --no-check-certificate $url
  lastfile=$(ls -r1 *.tgz | tail -n1)
  tar --exclude '*.pdf' --exclude '*zip' -xzvf $lastfile proceedings/order proceedings/final.tgz
  tar xzvf proceedings/final.tgz
  mv final proceedings
  cd -
  echo ''
done
