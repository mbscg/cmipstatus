#!/scratchin/prod/um/home/umrun/prj/xconv/convsh1.90_ifc_dynamic
#!/scratchin/prod/um/home/umrun/prj/xconv/convshR81.91

#  Abre automaticamente os arquivos (sem precisar especificar o tipo de arquivo)

set filetype 0

#  Escolhendo as variaveis (mesmas do convsh) 
# set fieldlist "24"
set fieldlist "{{ ind_var }}"

# Diretorio dos arquivos
# set dir /stornext/online14/ocean/simulations/exp120/dataout/ic12/ic2005/01/atmos/CGCM_MEAN
set dir {{ directory }}

#  Ler os arquivos 

set infile template.ctl
readfile $filetype $dir/$infile

#  Arquivo de saida

set lastpart [file tail $infile]
#set outfile cloud_cover_exp120.nc
set outfile {{ output_nc }}

#  Escrendo o arquivo da saida

writefile netcdf $outfile $fieldlist

clearall

