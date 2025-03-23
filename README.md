# LoRA-PEFT Stable Diffusion for Shoes Image Generation

This repository provides an implementation of fine-tuning **Stable Diffusion** using **LoRA (Low-Rank Adaptation)** and **PEFT (Parameter Efficient Fine-Tuning)** on a custom dataset of shoe images and captions. The dataset was collected through Selenium-based web scraping and later used for fine-tuning Stable Diffusion.

## Repository Structure

```
LoRA-PEFT_Stable_Diffusion/
│── Dataset/
│   ├── final_shoe_scraper.py
│   ├── final_shoe_scraper_multithreading.py
│   ├── myntra_link_scraper.py
│   ├── myntra_shoe_scraper.py
│── Fine_Tuning_Stable_Diffusion.ipynb
│── README.md
```

## Dataset Collection
The dataset was created using Selenium and Python scripts for web scraping. The `Dataset/` folder contains scripts to scrape shoe images and captions from **Myntra**.

The final dataset is publicly available on Hugging Face:
[**Myntra Shoes Dataset**](https://huggingface.co/datasets/Harshgarg12/myntra_shoes_dataset)

## Fine-Tuning Stable Diffusion
The fine-tuning process utilizes **LoRA-PEFT** to efficiently train Stable Diffusion on the collected dataset. The main notebook, `Fine_Tuning_Stable_Diffusion.ipynb`, provides a step-by-step approach to training the model.

The trained LoRA model is available on Hugging Face:
[**LoRA-PEFT Stable Diffusion - Myntra Shoes**](https://huggingface.co/Harshgarg12/LoRA_Peft_SD_Myntra_Shoes)

## How to Use
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/LoRA-PEFT_Stable_Diffusion.git
cd LoRA-PEFT_Stable_Diffusion
```

### 2. Install Dependencies
Ensure you have the required dependencies installed:
```bash
pip install -r requirements.txt
```

### 3. Running the Scraper
To scrape shoe images and descriptions from Myntra, run:
```bash
python Dataset/final_shoe_scraper.py
```
For a multithreaded version:
```bash
python Dataset/final_shoe_scraper_multithreading.py
```

### 4. Fine-Tune Stable Diffusion
Run the `Fine_Tuning_Stable_Diffusion.ipynb` notebook in a Jupyter environment to train the model using LoRA.

## Resources
- [CompVis/stable-diffusion-v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4)
- [diffusers/examples/text_to_image/train_text_to_image_lora.py](https://github.com/huggingface/diffusers/blob/main/examples/text_to_image/train_text_to_image_lora.py)
- [myntra_link_scraper.py](https://github.com/Architrixs/myntra_scraper/blob/main/myntra_link_scraper.py)

