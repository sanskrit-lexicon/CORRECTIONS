echo "create pdhw0.txt from pd.txt"
python hw0.py ../cologneDownloads/pdtxt/pd.txt pdhw0.txt > pdhw0_note.txt
echo "create hwchk_iast.txt from pdhw0.txt"
python hwchk_iast.py pdhw0.txt hwchk_iast.txt > hwchk_iast_log.txt
