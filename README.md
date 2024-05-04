# Font2Logo

![Sample Image](/img/Font2Logo.png)

## Requirements

- conda env (python 3.8 above)
- node

## Additional files to Download

2. Download Font2Logo's [Dataset](https://drive.google.com/file/d/1TTqAklfsAp6KOPxCVl2jktH8kN4lEmI_/view?usp=sharing) and put it in `Att2font/data`
3. Download the official pre-trained vgg19 model: [vgg19-dcbb9e9d.pth](https://download.pytorch.org/models/vgg19-dcbb9e9d.pth), and put it under `Att2font` project root folder
4. Download the pre-trained auto-encoder models from this [google drive](https://drive.google.com/file/d/13n_YJ6J8lIvF-liWFeJY35nXsZM-5vTZ/view?usp=sharing). Unzip and place them at path `.LogoGenerator/texture_models/`
5. Download [Log generator rar file](https://drive.google.com/file/d/1u79bqUv-yCoXHLFSe2vt_oRu5RS2-hxd/view?usp=sharing) and put the `dataset` and `experiments` folder in the `Logo_generator` folder
6. make these additional folders ` Attr2Font/experiments/att2font_en/results/* ;Logo_Generator/text_image/*  ;Attr2Font/data/explor_all/image/*`

## Execution

- install the python requirements with `pip install -r requirements.txt`
- run app.py for `Logo_generator` and `Attr2font`
- npm install in `vue-prime`
- npm run dev in `vue-prime`

## References

- hologerry [Attr2font](https://github.com/hologerry/Attr2Font)
- EndyWon [Texture-Reformer](https://github.com/EndyWon/Texture-Reformer)
- yizhiwang096 [TextLogoLayout](https://github.com/yizhiwang96/TextLogoLayout)
