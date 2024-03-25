# Font2Logo
## Requirements
- conda env (python 3.8 above)
- node 
## Additional files to Download

1. Download the [Attr2font experiments](https://drive.google.com/drive/folders/1M5Y170gyySNu6zZmNNdqNJG0JF_D2UBJ?usp=sharing) and place it as `Font2Logo/Attr2Font/experiments`
2. Download Font2Logo's [Dataset](https://drive.google.com/file/d/1TTqAklfsAp6KOPxCVl2jktH8kN4lEmI_/view?usp=sharing)and put it in `Att2font/data`
4. Download the official pre-trained vgg19 model: [vgg19-dcbb9e9d.pth](https://download.pytorch.org/models/vgg19-dcbb9e9d.pth), and put it under `Att2font` project root folder
5. Download the pre-trained auto-encoder models from this [google drive](https://drive.google.com/file/d/13n_YJ6J8lIvF-liWFeJY35nXsZM-5vTZ/view?usp=sharing). Unzip and place them at path `.LogoGenerator/texture_models/`
6. Download [Log generator rar file](https://drive.google.com/file/d/1u79bqUv-yCoXHLFSe2vt_oRu5RS2-hxd/view?usp=sharing) and put the `dataset` and `experiments` folder in the `Logo_generator` folder

## Execution
- install the python requirements with `pip install -r requirements.txt`
- run app.py for `Logo_generator` and `Attr2font`
- npm install in `Vueinterface`
- npm run dev in `Vueinterface` 
## References
- hologerry [Attr2font](https://github.com/hologerry/Attr2Font)
- EndyWon [Texture-Reformer](https://github.com/EndyWon/Texture-Reformer)
- yizhiwang096 [TextLogoLayout](https://github.com/yizhiwang96/TextLogoLayout)
