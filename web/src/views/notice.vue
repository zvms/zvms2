<template>
    <v-card>
        <v-card-title>创建通知</v-card-title>
        <v-card-text>
            <v-form ref="form">
                <v-simple-table>
                    <thead>
                        <td>班级</td>
                        <td></td>
                    </thead>
                    <tbody>
                        <tr v-for="(userId, i) in userSelected" :key="i">
                            <td>{{ mp[userId] }}</td>
                            <td>
                                <v-btn class="mx-2" fab dark x-small color="primary" @click="delFromList(i)">
                                    <v-icon dark>
                                        mdi-minus
                                    </v-icon>
                                </v-btn>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <v-select prepend-icon="mdi-switch" v-model="target_new" label="发送目标" :items="users"
                                    item-text="name" item-value="id">
                                </v-select>
                            </td>
                            <td>
                                <v-btn class="mx-2" fab dark x-small color="primary" @click="addToList">
                                    <v-icon dark>
                                        mdi-plus
                                    </v-icon>
                                </v-btn>
                            </td>
                        </tr>
                    </tbody>
                </v-simple-table>
                <v-text-field v-model="form.title" label="标题" :rules="rules"></v-text-field>
                <v-textarea v-model="form.message" :auto-grow="true" label="要发送的消息" :rules="rules"></v-textarea>
            </v-form>
            <v-dialog ref="dateDialog" v-model="modalDate" :return-value.sync="form.date" persistent width="290px">
                <template v-slot:activator="{ on, attrs }">
                    <v-text-field v-model="form.date" label="通知到期日期（默认持续三天）" prepend-icon="mdi-calendar" readonly
                        v-bind="attrs" v-on="on"></v-text-field>
                </template>
                <v-date-picker v-model="form.date" scrollable>
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="modalDate = false">
                        取消
                    </v-btn>
                    <v-btn text color="primary" @click="$refs.dateDialog.save(form.date)">
                        确认
                    </v-btn>
                </v-date-picker>
            </v-dialog>
            <v-card-actions>
                <v-btn color="primary" block @click="send">发送消息</v-btn>
            </v-card-actions>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { toasts } from "../utils/dialogs";
import { fApi, checkToken } from "../apis";
import { NOTEMPTY } from "../utils/validation";
import { mapIsLoading } from "@/stores";

export default {
    data() {
        return {
            form: {
                title: undefined,
                message: undefined,
                date: undefined
            },
            users: undefined,
            target_new: undefined,
            userSelected: [],
            mp: {},
            modalDate: false,
            rules: [NOTEMPTY()]
        }
    },
    mounted () {
        this.pageload()
    },
    methods: {
        async pageload() {
            await checkToken();
            let users = await fApi.fetchClassList();
            users
                ? (this.users = users)
                : toasts.error("获取班级列表失败");


            for (const cls of this.users)
                this.mp[cls.id] = cls.name;

        },
        addToList () {
            let flg = false;
            if (this.target_new == "") flg = true;
            for (const user of this.userSelected) {
                if (user["id"] == this.target_new) {
                    flg = true;
                    break;
                }
            }
            if (!flg)
                this.userSelected.push(this.target_new);
            this.target_new = "";
        },
        delFromList (i) {
            this.userSelected.splice(i, 1);
        },
        send: async function () {
            if (!this.userSelected || this.userSelected.length == 0) {
                toasts.error("请选择发送目标");
                return
            }

            if (!this.form.date) {
                const d = new Date()
                this.form.date = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + (d.getDate() + 2)
            }

            let data = await fApi.sendNotice(
                this.userSelected,
                this.form.title,
                this.form.date,
                this.form.message
            );
            if (data.type == "SUCCESS") {
                toasts.success(data.message);
                for (let k in this.form)
                    this.form[k] = undefined
                this.userSelected = []
            } else {
                toasts.error(data.message);
            }
        }
    },
    computed:{
        ...mapIsLoading()
    }
}
</script>