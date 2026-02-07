from transformers import AutoModelForCausalLM, AutoTokenizer

class TextGeneratorService:
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
    
    grammar_instruct = "You are a helpful assistant which helps to generate single short example sentences using a grammar provided in a grammar sheet."
    grammar_shots = [
        ["""# Énumérer avec 第 dì\n\n第 dì permet de former des chiffres et nombres ordinaux.
        Il s'emploie de la façon suivante :

        第 + chiffre/nombre ( + Classificateur )

        * 第一 dì yī : « Le premier »
        * 第二 dì èr : « Le deuxième »
        * 第三 dì sān : « Le troisième »
        * 我是第四 wǒ shì dì sì : « Je suis quatrième »
        * 他是第六 tā shì dì liù : « Il est sixième »

        Nous pouvons également y rajouter un classificateur, puis un nom :

        * 第一个月 dì yī gè yuè : « Le premier mois »
        * 我是第三个人 wǒ shì dì sān gè rén : « Je suis la troisième personne »
        * 我的第三个中文老师 wǒ de dì sān gè zhōngwén lǎoshī : « Mon troisième professeur de chinois »
        * 第一次 dì yī cì : « La première fois »
        * 这是我第三次吃中国饭 zhè shì wǒ dì sān cì chī zhōngguó fàn : « C’est la troisième fois que je mange chinois »

        Le classificateur est absent pour, entre autres, les mots 天 tiān et 年 nián :

        * 第一天 dì yī tiān : « Le premier jour »
        * 第二年 dì èr nián : « La deuxième année »

        Lorsque l'on veut dire « deuxième », il faut employer 二 èr et non 两 liǎng :

        * 两个人 liǎng gè rén : « Deux personnes »
        * 第二个人 dì èr gè rén : « La deuxième personne »

        Les deux mots suivants signifient « étage » et peuvent s'employer sans 第 dì :

        * 三楼 sān lóu : « Troisième étage »
        * 四层 sì céng : « Quatrième étage »""", "这是我第二次来中国。"],
        ["""# Exprimer une distance avec 离 lí

        离 lí est utilisé lorsqu'on souhaite exprimer une distance entre deux points. Il peut se traduire par « par rapport à ». La structure à employer, très différente du français, est la suivante :

        Lieu A + 离 + Lieu B + Adverbe + Adjectif

        * 这个地方离那个地方不远 zhè gè dìfāng lí nà gè dìfāng bù yuǎn : « Cet endroit-ci n’est pas loin de cet endroit-là »
        * 我的家离你的家不远 wǒ de jiā lí nǐ de jiā bù yuǎn : « Ma maison n’est pas loin de la tienne »
        * 你的家离市中心远吗？nǐ de jiā lí shìzhōngxīn yuǎn ma ? : « Ta maison est-elle loin du centre-ville ? »
        * 这里离公交车站远不远？zhè lǐ lí gōngjiāochē zhàn yuǎn bù yuǎn ? : « L’arrêt de bus est-il loin d’ici ? »
        * 火车站离我的家比较近 huǒchē zhàn lí wǒ de jiā bǐjiào jìn : « La gare est plutôt proche de chez moi »
        * 火车站离这儿太远了 huǒchē zhàn lí zhèr tài yuǎn le : « La gare est trop éloignée d’ici »
        * 酒吧离我的家比较远 jiǔbā lí wǒ de jiā bǐjiào yuǎn : « Le bar est plutôt loin de chez moi »""", "这栋房子离公园不远。"]
    ]

    vocabulary_instruct = "You are a helpful assistant which helps to generate single short example sentences using a vocabulary word provided."
    vocabulary_shots = [
        ["吃饭", "我喜欢吃中国饭。"],
        ["学习", "我每天学习中文。"],
        ["朋友", "我的朋友很友好。"]
    ]

    calligraphy_instruct = "You are a helpful assistant which helps to generate a single example word using a character provided."
    calligraphy_shots = [
        ["学", "学习"],
        ["语", "语言"],
        ["文", "文化"]
    ]

    def generate_learnable_sentence(self, grammar_sheet: str) -> str:
        """
        Generate a learnable sentence based on a grammar sheet.
        
        Args:
            grammar_sheet: The grammar sheet to use for generating the sentence.
        
        Returns:
            A single short example sentence that illustrates the grammar point.
        """

        messages = [
            {"role": "system", "content": self.grammar_instruct}
        ]

        for grammar_shot, sentence_shot in self.grammar_shots:
            messages.append({"role": "user", "content": grammar_shot})
            messages.append({"role": "assistant", "content": sentence_shot})

        messages.append({"role": "user", "content": grammar_sheet})
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=128,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    def generate_example_sentence(self, vocabulary_word: str) -> str:
        """
        Generate an example sentence based on a vocabulary word.
        
        Args:
            vocabulary_word: The vocabulary word to use in the example sentence.
        
        Returns:
            A single short example sentence that illustrates the vocabulary word.
        """

        messages = [
            {"role": "system", "content": self.vocabulary_instruct}
        ]

        for vocabulary_shot, sentence_shot in self.vocabulary_shots:
            messages.append({"role": "user", "content": vocabulary_shot})
            messages.append({"role": "assistant", "content": sentence_shot})

        messages.append({"role": "user", "content": vocabulary_word})
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=128,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    def generate_example_word(self, character: str) -> str:
        """
        Generate an example word based on a character.
        
        Args:
            character: The character to use in the example word.
        
        Returns:
            A single example word that contains the character.
        """

        messages = [
            {"role": "system", "content": self.calligraphy_instruct}
        ]

        for calligraphy_shot, word_shot in self.calligraphy_shots:
            messages.append({"role": "user", "content": calligraphy_shot})
            messages.append({"role": "assistant", "content": word_shot})

        messages.append({"role": "user", "content": character})
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=16,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]