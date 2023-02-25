<!--
 * @Author: Alchemistyui
 * @Date: 2023-02-20
 * @LastEditTime: 2023-02-25
 * @FilePath: /Text2UI_WebLabeler/src/WebLabeler.vue
 * @Description: 
 * 
 * Copyright (c) 2023, All Rights Reserved. 
-->
<template>
    <div class="tool_header">
        <img alt="Vue logo" class="logo" src="@/assets/logo.png" width="125" height="125" />
        <h1 class="header_title">Annotation Tool</h1>
    </div>

    <p v-if="auto_mode" style="color: #FF60AF; font-size: large; margin: 20px auto; width:700px; text-align: center;">
        Auto mode is on... <br> Will write desktop & mobile with same annotation once.
    </p>

    <div style="margin: 0 auto; width: 85%;">
        <el-form ref="form" :model="form" label-width="auto">
            <el-form-item label="* File Name" style="text-align: center;">
                <p class="input_hint">marlon_profile_01_1.png</p>
                <el-input v-model="form.file_name" :disabled="formSubmitted" />
            </el-form-item>
            <el-form-item label="* Web Category" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                <p class="input_hint">desktop view, personal page / functional <p v-if="!auto_mode">/ mobile view, personal page</p> </p>
                <el-input v-model="form.category" :disabled="formSubmitted" />
            </el-form-item>
            <el-form-item label="Web Main Color List">
                <p class="input_hint">white, blue</p>
                <el-input v-model="form.color" :disabled="formSubmitted" />
            </el-form-item>
            <!-- full path should be: train_elements + file_name.split('_')[0] + file name +'.png' -->
            <el-form-item label="Elements Image Name List">
                <div class="tag-list">
                    <el-tag v-for="tag in form.tags" :key="tag" closable @close="removeTag(tag)">
                    {{ tag }}
                </el-tag>
                <el-input v-model="newTag" class="input-new-tag" ref="addTagInput" placeholder="Add tag"
                        @keyup.enter="addTag" size="small" maxlength="20">
                        <el-button slot="append" icon="el-icon-circle-plus-outline" @click="addTag"></el-button>
                    </el-input>
                </div>
            </el-form-item>

            <el-form-item label="* Simple Description">
                <p class="input_hint"> a breakfast and restaurant website, landing page</p>
                <el-input v-model="form.description" autosize type="textarea" :disabled="formSubmitted" />
            </el-form-item>


            <el-form-item label="* Text Contents">
                <el-table :data="form.tableData">
                    <el-table-column label="Key" prop="key" min-width="60%"></el-table-column>
                    <el-table-column label="Value" prop="value" min-width="200%">
                        <template v-slot="scope">
                            <el-input v-model="scope.row.value" autosize type="textarea"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column label="Action">
                        <template v-slot="scope">
                            <el-button type="text" size="small" min-width="20%" @click="removeTableRow(scope.$index)">
                                Remove
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>


                <div style="display: flex; margin-top: 10px;">
                    <el-input v-model="newItem" ref="addItemInput" placeholder="Add New Key" @keyup.enter="addTableRow"
                        size="small" maxlength="20">
                    </el-input>
                    <!-- <el-button size="small" @click="addTableRow" style="margin-left: 20px;">Add Row</el-button> -->
                </div>

            </el-form-item>




            <div class="submit-container">
                <el-button type="primary" @click="submitForm" :disabled="formSubmitted"
                    style="width: 200px;">Submit</el-button>
            </div>
        </el-form>
    </div>
</template>


<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

// used for initial when upload a data
const initial_val = {
                file_name: 'beats_01_1.png',
                category: 'desktop view, ecommerce',
                color: 'black, dark, white',
                description: '',
                tags: ['logo'],
                // tags: [],
                tableData: [
                    { key: 'nav_bar', value: 'logo image, Home, Specs, Case, Products' },
                    { key: 'title', value: '' },
                    { key: 'description', value: '' },
                    { key: 'button', value: '' }
                ]
            }
const mobile_nav_bar = "logo image, Menu_icon"

export default {
    name: 'WebLabeler',
    data() {
        return {
            auto_mode: true,
            form: {
                file_name: 'beats_01_1.png',
                category: 'desktop view, ecommerce',
                color: 'black, dark, white',
                description: '',
                tags: ['logo'],
                // tags: [],
                tableData: [
                    { key: 'nav_bar', value: 'logo image, Home, Specs, Case, Products' },
                    { key: 'title', value: '' },
                    { key: 'description', value: '' },
                    { key: 'button', value: '' }
                ]
            },
            newTag: "",
            newItem: "",
            formSubmitted: false
        };
    },
    methods: {

        addTag() {
            if (this.newTag) {
                this.form.tags.push(this.newTag);
                this.newTag = "";
                this.$nextTick(() => {
                    this.$refs.addTagInput.$refs.input.focus();
                });
            }
        },
        removeTag(index) {
            this.form.tags.splice(index, 1);
        },


        addTableRow() {
            // this.form.tableData.push({ key: this.form.newItem, value: '' });
            if (this.newItem) {
                this.form.tableData.push({ key: this.newItem, value: '' });
                this.newItem = '';
            }
        },
        removeTableRow(index) {
            this.form.tableData.splice(index, 1);
        },

        checkForm(text_contents) {
            var valid_text = true
            for (var key in text_contents) {
                if (!text_contents[key]) {
                    valid_text = false
                }
            }
            // remove this.form.tags.length == 0, some may don't have image
            if (!this.form.file_name || !this.form.category 
                    || !this.form.description || !valid_text) {
                ElMessage.error('Please fill out all required fields');
                return false;
            }
            return true;
        },

        submitForm() {
            var text_contents = {}
            for (var i = 0; i < this.form.tableData.length; i++) {
                var item = this.form.tableData[i]
                text_contents[item['key']] = item['value']
            }
            if (!this.checkForm(text_contents)) {
                return;
            }
            
            // console.log(this.form.tags.values());
            const form_data_desktop = {
                file_name: this.form.file_name,
                annos: {
                    category: this.form.category,
                    main_color: this.form.color,
                    elements: this.form.tags,
                    description: this.form.description,
                    text_contents: text_contents
                }
            }
            // console.log(JSON.stringify(form_data));

            axios.post('http://localhost:8000/submit', form_data_desktop)
            

            if ("nav_bar" in text_contents) {
                // delete text_contents.nav_bar
                text_contents['nav_bar'] = mobile_nav_bar
            }
            const form_data_mobile = {
                file_name: this.form.file_name.replace('_1', '_2'),
                annos: {
                    category: this.form.category.replace('desktop', 'mobile'),
                    main_color: this.form.color,
                    elements: this.form.tags,
                    description: this.form.description,
                    text_contents: text_contents
                }
            }
            // console.log(form_data_desktop)
            axios.post('http://localhost:8000/submit', form_data_mobile)
                .then(response => {
                    ElMessage.success('Form submitted successfully');
                    // console.log(initial_val)
                    this.form = initial_val
                })
                .catch(error => {
                    ElMessage.error('Form submission failed');
                    console.error(error);
                });
            // }
            
        }
    }
};
</script>
  

<style>
.header_title {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
    /* background-color: #333; */
    /* color: #333; */
    font-size: 2rem;
    margin: 0;
    /* this removes any margin added by default */
}

.logo {
    width: 100px;
    /* adjust the width to your desired size */
    height: 100px;
    /* adjust the height to your desired size */
    border-radius: 40%;
    /* this will make the image a circle */
    object-fit: cover;
    /* this ensures the image fills the circle without distortion */
    display: block;
    margin: 0 auto 2rem;
    margin-right: 30px;
}

.tool_header {
    width: 600px;
    /* display: grid; */
    display: flex;
    align-items: center;
    /* grid-template-columns: 1fr 1fr; */
    padding: 0 2rem;
    margin: 0 auto;
}

.input_hint {
    color: #7B68EE;
}

.submit-container {
    display: flex;
    justify-content: center;
    margin-top: 50px;
}
</style>
  

