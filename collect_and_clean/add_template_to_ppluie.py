##additions to make in the ppluie library

## in supported_templates 
    "DETECTREV"


## in make_prompt():
    
        case "DETECTREV":
            template = [
                {"role": "user", "content": "You will receive two paragraphs P1 and P2. P2 is a final version of a paragraph written for a scientific article, and P1 is suspected to be an original version of P2 before revision."
                +" Can the P2 paragraph or a part of it be qualified as a revision of P1?"
                +" If the changes only affect equations or if here is too much equations it is not considered a revision."
                +" Answer with only one word \"Yes\" or \"No\"."},
                {"role": "assistant", "content": "Please provide the data for me to evaluate."},
            ]

            template.append({"role": "user", "content": "P1: \""+hypothese+"\"; P2: \""+reference+"\""})

            yes = [v for v in template]
            no = [v for v in template]
            yes.append({"role": "assistant", "content": "Yes"})
            no.append({"role": "assistant", "content": "No"})
            return yes,no
        case "FINSTRUCT":
            template = [
                {"role": "user", "content": "You will receive two paragraphs P1 and P2 and an instruction I. P1 is a paragraph written for a scientific article, I is an instruction on how to revise P1 and P2 is a revised version of P1."
                #+" Do these two sentences mean the same thing?"
                +" Did P2 addressed the instruction I?"
                +" Answer with only one word \"Yes\" or \"No\"."},
                {"role": "assistant", "content": "Please provide the data for me to evaluate."},
            ]
            template.append({"role": "user", "content": "P1: \""+reference+"\"; I: \""+instruction+"\"; P2: \""+gold+"\""})
            template.append({"role": "assistant", "content": "Yes"})

            template.append({"role": "user", "content": "P1: \""+reference+"\"; I: \""+instruction+"\"; P2: \""+hypothese+"\""})

            yes = [v for v in template]
            no = [v for v in template]
            yes.append({"role": "assistant", "content": "Yes"})
            no.append({"role": "assistant", "content": "No"})
            return yes,no
