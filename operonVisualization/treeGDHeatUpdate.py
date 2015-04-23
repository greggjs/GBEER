import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cbook as cbook
from matplotlib._png import read_png
from matplotlib.offsetbox import OffsetImage 
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from Bio import Phylo
from mpl_toolkits.axes_grid1 import make_axes_locatable,Size
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib import cm
from PIL import Image
from os.path import expanduser
import os
import ntpath
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FixedLocator
import pickle
from matplotlib.colors import ColorConverter
from reportlab.lib import colors
from os.path import split

#defines a red-blue colormap 
def blueredcmap():
    BlueRed = {
               'red':  ((0.0, 0.0, 0.0),
                       (0.25,0.0, 0.0),
                       (0.5, 0.8, 1.0),
                       (0.75,1.0, 1.0),
                       (1.0, 0.4, 1.0)),

               'green':((0.0, 0.0, 0.0),
                       (0.25,0.0, 0.0),
                       (0.5, 0.9, 0.9),
                       (0.75,0.0, 0.0),
                       (1.0, 0.0, 0.0)),

               'blue': ((0.0, 0.0, 0.4),
                       (0.25,1.0, 1.0),
                       (0.5, 1.0, 0.8),
                       (0.75,0.0, 0.0),
                       (1.0, 0.0, 0.0))
              }
    return BlueRed

#produces a heatmap axis with a color bar
def produceHeat(fig,gridspace3,max_num, min_num, full_len, txtnames):
    mpl.rcParams['xtick.minor.pad']='8'
    font= mpl.rcParams['font.size']=14.0 
    absolute_max=abs(max_num)
    absolute_min=abs(min_num)
    cb_boundary=max(absolute_max,absolute_min)
    BlueRed=blueredcmap()
    plt.register_cmap(name='BlueRed', data=BlueRed)
    norm = mpl.colors.Normalize(vmin=-3.0, vmax=3.0)
    cmap = plt.get_cmap('BlueRed')
    masked_array = np.ma.masked_where(full_len==np.NaN,full_len)
    cmap.set_bad('green',1.0)
    ##rect_ht = [0,0.3 , 0.5, 0.8]
    ht_ax=fig.add_subplot(gridspace3)
    ##ht_ax = plt.axes(rect_ht)    
    ht_ax.set_xlim(0,len(txtnames))
    ht_ax.set_ylim(0,len(txtnames))
    divider = make_axes_locatable(ht_ax)
    cbax = divider.append_axes("right", size="5%", pad=0.10)
    img = ht_ax.imshow(masked_array, cmap=cmap, interpolation='nearest',aspect='auto',
                 vmin=-cb_boundary,vmax=cb_boundary,extent=[len(txtnames),0,len(txtnames),0],
                 origin='lower')
    majorLocator = MultipleLocator(1)
    minorticks = np.arange(-2.5,len(txtnames),step=1.0)
    minorLocator = FixedLocator(minorticks[3:])
    ht_ax.xaxis.set_major_locator(majorLocator)
    ht_ax.yaxis.set_major_locator(majorLocator)
    ht_ax.xaxis.set_minor_locator(minorLocator)
    ht_ax.grid(True, which='major')
    ht_ax.set_xticklabels(txtnames, minor=True,rotation=90)
    plt.setp(ht_ax.get_xmajorticklabels(),visible=False)
    plt.setp(ht_ax.get_yticklabels(),visible=False)    
    plt.setp(ht_ax.get_xticklines(),visible=False)
    plt.setp(ht_ax.get_yticklines(),visible=False)
    plt.colorbar(img, cax=cbax)
    return ht_ax

# produces a tree axis with Bio.Phylo returning a matplotlib axis
# TODO: Each rectangle's co-ordinates needs to be determined via a 
#       function which is able to distinguish between different categories 
#       of proteobacteria (alpha,gamma,delta,epsilon,beta).
def producePhylo(fig,gridspace1,tree_path):
    font= mpl.rcParams['font.size']=13.0    
    tree=Phylo.read(tree_path,"newick")    
    phyl_ax=fig.add_subplot(gridspace1)
    ##uncomment the next 4 lines to add rectangles on the tree
    ##phyl_ax.add_patch(Rectangle((5.6,16.7),10.2,16.8,edgecolor="brown", fill=False))
    ##phyl_ax.add_patch(Rectangle((5.6,9.5),10.2,6.8,edgecolor="magenta", fill=False))
    ##phyl_ax.add_patch(Rectangle((5.6,6.6),10.2,2.6,edgecolor="black", fill=False))
    ##phyl_ax.add_patch(Rectangle((5.6,0.4),10.2,5.9,edgecolor="turquoise", fill=False))
    Phylo.draw(tree, axes=phyl_ax, do_show=False,show_confidence=False)
    phyl_ax.set_xlim(0,16)
    phyl_ax.set(xlabel='',ylabel='')
    plt.setp(phyl_ax.get_xticklabels(),visible=False)
    plt.setp(phyl_ax.get_yticklabels(),visible=False)
    plt.setp(phyl_ax.get_xticklines(),visible=False)    
    plt.setp(phyl_ax.get_yticklines(),visible=False)
    return phyl_ax

# produces a genome diagram axis using Image and later clipping the 
# extra white space around the GD, plots the resulting image with imshow
def imshowGD(fig,gridspace2,gdiag):
    ##print gdiag
    ##rect_gd = [-0.47, 0.3, 0.6, 0.8]
    gd_ax=fig.add_subplot(gridspace2)    
    ##gd_ax = plt.axes(rect_gd,frameon=True)    
    gdiag_img=Image.open(gdiag)
    np_gd = np.asarray(gdiag_img)
    np_gd = np_gd[:,:,0:3]
    idx = np.where(np_gd-255)[0:2]
    box = map(min,idx)[::-1] + map(max,idx)[::-1]
    region = gdiag_img.crop(box)
    region_pix = np.asarray(region)    
    gd_ax.imshow(region_pix,interpolation='bilinear', aspect="auto")
    plt.setp(gd_ax.get_xticklabels(),visible=False)
    plt.setp(gd_ax.get_yticklabels(),visible=False)
    plt.setp(gd_ax.get_xticklines(),visible=False)    
    plt.setp(gd_ax.get_yticklines(),visible=False)
    return gd_ax

# returns a axis with legend information
# gene name: color coded rectangle
def legendDrawing(fig, gridspace4, geneToColorDict,gd,operon):
    legend_ax=fig.add_subplot(gridspace4)
    Gene_num=len(geneToColorDict)
    Row_num=Gene_num/3
    legend_ax.set_xlim(0,3)
    legend_ax.set_ylim(3,0)
    geneList=geneToColorDict.keys()
    x = 0.1
    y = 0.1
    patches = []
    for i,gene in enumerate(geneList):
        color_str=geneToColorDict[gene]

        if i==0 or i % 3!= 0:
##           ##bb = FancyArrow(x,y,0.1,0.0,length_includes_head=True, width=0.05, 
##                        head_length=0.03, head_width=0.05, fc=color_str, ec=color_str,
##                        lw=4)
           bb = Rectangle((x,y),0.2,0.05,color =color_str, fill=True)             
           legend_ax.annotate(gene, (x+0.26,y+0.05),size = 15)       
           legend_ax.add_artist(bb)
           x=x + 1
        else:
           y=y + 0.1
           x = 0.1
##           ##bb = FancyArrow(x,y,0.1,0.0,length_includes_head=True, width=0.05, 
##                        head_length=0.03, head_width=0.05, fc=color_str, ec=color_str,
##                        lw=4)
           bb = Rectangle((x,y),0.2,0.05, color =color_str, fill=True)             
           legend_ax.annotate(gene, (x+0.26,y+0.05),size = 15)      
           legend_ax.add_artist(bb)
           x=x + 1
    legend_ax.annotate(operon, (1.0,1.25),size = 30)
    legend_ax.axis("off")
    return legend_ax    

    
def traverseAll(path):
    res=[]
    for root,dirs,files in os.walk(path):
        for f in files:
            res.append(root+"/"+f)
    return res

##def determineDirectory():
##    home = expanduser("~")
##    try:
##        joined_path=os.path.join(home,"Desktop","combined")
##        if not os.path.exists(joined_path):
##               os.makedirs(joined_path)
##    except OSError as exception:
##        if exception.errno != errno.EEXIST:
##           raise
##    return joined_path    


def combineAll(max_num, min_num, full_len, txtnames, tree_path, operon, gd_files_list, joined_path, pickleDict):
    fig = plt.figure(figsize=(30,40))
    heatmapGS = gridspec.GridSpec(2,3,wspace=0.0,hspace=0.0,width_ratios=[0.40,1,1],height_ratios=[1,1,1])
    ##heatmapGS = gridspec.GridSpec(2,2,wspace=0.0,hspace=0.0,width_ratios=[0.40,1],height_ratios=[1,1])
    phyl_ax = producePhylo(fig,heatmapGS[0,0],tree_path)
    for gd in gd_files_list:
        ##print "actual_gd:", gd
        ##print "operon:", operon
        ##print "split_gd:", ntpath.basename((gd.split("/")[3]).split(".")[0])
        ##print "split_operon:", operon.split("_")[0]
        head, tail = os.path.split(gd) 
        operonName = tail.split(".")[0]       
        if operonName == operon.split("_")[0]:
           ##print pickleDict.keys()
           ##print ntpath.basename((gd.split("/")[3]).split(".")[0])
           geneToColorDict = pickleDict[operonName]
           gd_ax = imshowGD(fig,heatmapGS[0,1],gd)
           legend_ax = legendDrawing(fig,heatmapGS[1,1],geneToColorDict,gd,operon)
           break
   
    ht_ax = produceHeat(fig,heatmapGS[0,2], max_num, min_num, full_len, txtnames)
    fig.savefig(os.path.join(joined_path,operon+".png"), format = 'png'
                 ,bbox_inches='tight',dpi=120)
    plt.close(fig)
    return
