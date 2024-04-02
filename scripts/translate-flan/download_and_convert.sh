curl https://object.pouta.csc.fi/Tatoeba-MT-models/eng-nor/opus+bt-2021-04-20.zip --create-dirs -o models/eng-nor/opus+bt-2021-04-20.zip
curl https://object.pouta.csc.fi/Tatoeba-MT-models/eng-swe/opus+bt-2021-04-14.zip --create-dirs -o models/eng-swe/opus+bt-2021-04-14.zip
curl https://object.pouta.csc.fi/Tatoeba-MT-models/swe-eng/opus+bt-2021-04-30.zip --create-dirs -o models/swe-eng/opus+bt-2021-04-30.zip
curl https://object.pouta.csc.fi/Tatoeba-MT-models/nor-eng/opus-2021-02-18.zip --create-dirs -o models/nor-eng/opus-2021-02-18.zip
unzip models/eng-nor/opus+bt-2021-04-20.zip -d models/eng-nor/
unzip models/eng-swe/opus+bt-2021-04-14.zip -d models/eng-swe/
unzip models/swe-eng/opus+bt-2021-04-30.zip -d models/swe-eng/
unzip models/nor-eng/opus-2021-02-18.zip -d models/nor-eng/

ct2-opus-mt-converter --model_dir models/eng-nor/ --output_dir models/ct2/eng-nor/
ct2-opus-mt-converter --model_dir models/eng-swe/ --output_dir models/ct2/eng-swe/
ct2-opus-mt-converter --model_dir models/swe-eng/ --output_dir models/ct2/swe-eng/
ct2-opus-mt-converter --model_dir models/nor-eng/ --output_dir models/ct2/nor-eng/