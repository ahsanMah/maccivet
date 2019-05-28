# Mac(aque) CIVET CLI
> Pronounced (maak)civet
CLI wrapper for CIVET pipeline modified for macaque brain scans

## Usage

``` bash
$ cli.py [-h] [-p PARAMFILE] [-in INPUTDIR] [-out OUTPUTDIR]
              t1_image seg_label sub_label
```
### Positional arguments

| Name            | Description   |
| :-------------- |:-------------:|
  t1_image        |      T1-weighted input image
  seg_label       |     label file that defines all the segmentations
  sub_label       |      label file for subcortical structures like the
                        hippocampus
