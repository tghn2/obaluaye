export default {
    common: {
        title: "The Global Health Network Study Builder",
    },
    seo: {
        title: "The Global Health Network Study Builder",
        description: "The collaborative global health research study builder and support companion",
    },
    nav: {
        home: "Home",
        search: "Search",
        pathways: "Study pathways",
        comments: "Comments",
        groups: "My studies",
        settings: "Settings",
        about: "About",
        privacy: "Privacy",
        contact: "Contact",
        authentication: "Authentication",
        blog: "Blog",
    },
    header: {
        edit: "Edit",
        save: "Save",
        saving: "Saving",
        reset: "Reset",
        delete: "Delete",
        cancel: "Cancel",
    },
    footer: {
        rights: "All rights reserved.",
    },
    authentication: {
        roles: {
            custodian: "Admin",
            curator: "Team lead",
            researcher: "Team member",
            viewer: "Viewer",
        },
    },
    settings: {
        name: "Settings",
        description: "Update your personal settings, or delete your account.",
        nav: {
            pathway: "Personal profile",
            profile: "Profile",
            account: "Account",
            invitations: "Invitations",
            security: "Security",
            moderation: "Moderation",
        },
        pathway: {
            title: "Personal profile",
            description: "Review and manage your personal profile.",
        },
        account: {
            title: "User settings",
            description: "Changing your email address will change your login. Any changes will require you to enter your original password.",
            passwordRequired: "You will need to set a password ('Security') before you can save your profile changes.",
            accountPassword: "Original password",
            profileName: "Your name",
            email: "Email address",
            submit: "Submit",
        },
        invitations: {
            title: "Team invitations",
            description: "Accept or reject invitations to join study teams.",
            completePathway: "You cannot participate in a study team until you have completed a personal profile pathway.",
            invited: "Invited",
            for: "For",
            by: "By",
            accept: "Accept",
            reject: "Reject",
        },
        security: {
            title: "Security",
            description: "Secure your account by adding a password, or enabling two-factor security. Or both.",
            passwordRequired: "Any changes will require you to enter your original password.",
            totpOffer: "Secure your account further by enabling two-factor security.",
            accountPassword: "Original password",
            useTotp: "Use two-factor security",
            useTotpSetting: "Use TOTP settings",
            new: "New password",
            repeat: "Repeat new password",
            enableTotp: "Enable two-factor security",
            totpHelp1: "Download an authenticator app that supports Time-based One-Time Password (TOTP) for your mobile device.",
            totpHelp2Scan: "Open the app and scan the QR code below to pair your mobile with your account.",
            totpHelp2Type: "If you can't scan, you can type in the following key:",
            totpHelp3: "Enter the code generated by your Authenticator app below to pair your account:",
            totpHelp3Code: "6-digit verification code",
            cancel: "Cancel",
        },
    },
    start: {
        pathwayTitle: "Study pathways",
        pathwayDescription: "View a list of study pathways you can start.",
        groupTitle: "Study team",
        groupDescription: "Join or start a study team",
        commentTitle: "Comments",
        commentDescription: "See activity in your study teams",
        personalTitle: "Complete a personal profile",
        personalDescription: "Once complete, you can join study teams and start a study pathway",
    },
    filter: {
        filter: "Filter",
        filters: "Filters",
        clear: "Clear",
        search: "Search",
        refresh: "Refresh filters",
        dates: "Date range",
        to: "to",
        complete: "Completed",
        featured: "Featured",
        language: "Language",
    },
    multi: {
        untagged: "untagged",
        previous: "Previous",
        next: "Next",
    },
    group: {
        name: "Study team",
        new: "New study team",
        empty: "Nothing right now. Create a study team to see them here.",
        emptyIncomplete: "Once you complete a personal profile, you can participate in study teams.",
        create: "Create a study team",
        creating: "Creating study team",
        updating: "Updating study team",
        complete: "Complete",
        field: {
            title: "Title",
            description: "Description",
            subjects: "Keywords",
            country: "Country",
            spatial: "Region",
            language: "Language",
        },
        nav: {
            pathway: "My study",
            response: "Review your study",
            metadata: "Study team",
            members: "Study members",
            invitations: "Invitations",
        },
        pathway: {
            title: "My study",
            description: "Review and manage your study.",
        },
        members: {
            since: "Since",
            name: "Name",
            email: "Email",
            responsibility: "Responsibility",
            remove: "Remove",
        },
        roles: {
            viewer: "Viewer",
            researcher: "Team member",
            curator: "Team lead",
            custodian: "Admin",
        },
        invitations: {
            note: "Note: you must email this person so they know what this is for",
            placeholder: "Invite team member by email",
            invite: "Invite",
        },
        help: {
            title: "",
            description: "A complete description of the study team.",
            subjects: "A list of keywords for the study team. Comma-separated.",
            country: "A list of one or more countries appropriate to this study team.",
            spatial: "Regional characteristics of the study team.",
            language: "Specify study team communication language.",
        },
        alert: {
            createSuccessTitle: "Success",
            createSuccessContent: "Study created.",
            createErrorTitle: "Creation error",
            createErrorContent: "Study team creation failed. Please check your details, or internet connection, and try again.",
            saveErrorTitle: "Save error",
            saveErrorContent: "Study team failed to save. Please check your details, or internet connection, and try again.",
            removeErrorTitle: "Deletion error",
            removeErrorContent: "Could not remove study team. Please check your details, or internet connection, and try again.",
        },
    },
    pathway: {
        name: "Study pathway",
        new: "New study pathway",
        empty: "Nothing right now. Create some study pathways to see them here.",
        create: "Create a study pathway",
        creating: "Creating study pathway",
        updating: "Updating study pathway",
        translate: "Translating",
        metadata: "Metadata",
        publish: "Publish",
        unpublish: "Unpublish",
        download: "Download",
        upload: "Upload",
        field: {
            title: "Title",
            type: "Type",
            description: "Description",
            subjects: "Keywords",
            country: "Country",
            spatial: "Region",
            temporal: "Time period",
            language: "Language",
            citation: "Bibliographic citation",
            resources: "Resources",
        },
        types: {
            personal: "Personal profile",
            research: "Study",
        },
        help: {
            title: "",
            description: "A complete description of the study pathway.",
            subjects: "A list of keywords of the study pathway. Comma-separated. Contains all languages.",
            country: "A list of one or more countries appropriate to this study pathway.",
            spatial: "Regional information of the study pathway.",
            temporal: "Time period of the study pathway.",
            language: "Specify study pathway base language. Permits translation.",
            citation: "A bibliographic reference for the study pathway.",
        },
        alert: {
            saveErrorTitle: "Save error",
            saveErrorContent: "Study pathway failed to save. Please check your details, or internet connection, and try again.",
            removeErrorTitle: "Deletion error",
            removeErrorContent: "Could not remove study pathway. Please check your details, or internet connection, and try again.",
            toggleSuccessTitle: "Toggle success",
            toggleSuccessContent: "Publication state successfully changed.",
        },
        journey: {
            start: "Start",
            continue: "Continue",
            groupFor: "Study team for ",
            review: "Review",
            startPersonal: "Begin your personal profile.",
            startResearch: "Create a new study pathway for you or a team.",
            resources: "Help & resources",
            save: "Save & Close",
            saveNext: "Save & Next",
            saving: "Saving",
            previous: "Back",
            next: "Next",
        },
    },
    theme: {
        name: "Study step",
        new: "New study step",
        field: {
            title: "Title",
            description: "Description",
            subjects: "Keywords",
            country: "Country",
            spatial: "Region",
            language: "Language",
            nodes: "Nodes",
            resources: "Resources",
        },
        help: {
            title: "",
            description: "A complete description of the study step.",
            subjects: "A list of keywords of the study step. Comma-separated. Contains all languages.",
            country: "A list of one or more languages appropriate to this study step.",
            spatial: "Region of the study step.",
        },
    },
    node: {
        name: "Node",
        new: "New node",
        field: {
            question: "Question",
            subjects: "Keywords",
            resources: "Resources",
        },
        help: {
            question: "",
            subjects: "A list of keywords of the node. Comma-separated. Contains all languages.",
        },
    },
    form: {
        name: "Response type",
        new: "Add response option",
        required: "Required",
        randomise: "Randomise",
        select: "Select",
        terms: {
            name: "Options",
            value: "Text",
        },
        types: {
            value: "Text",
            valuerange: "Range",
            scale: "Scale",
            boolean: "True/false",
            selectone: "Select one",
            selectmany: "Select many",
            selectbranch: "Select branch",
            upload: "Upload",
        },
        responsevalue: "Response data type",
        scaleTo: "to",
        scaleLabel: "Label (optional)",
        branchNone: "Add a study step to branch",
        booleanTrue: "True",
        booleanFalse: "False",
        uploadText: "Upload your response.",
        valueText: "Respond with a",
        values: {
            date: "Date",
            datetime: "Date and time",
            year: "Year",
            number: "Number",
            integer: "Integer",
            boolean: "True/false",
            array: "List",
            string: "Text",
        },
        constraints: {
            dtype: "Data type",
            limit: "Limit",
            range: "Range",
            minimum: "Minimum",
            maximum: "Maximum",
        },
        example: "Example",
        upload: {
            upload: "Upload",
            drag: "or drag and drop",
            afile: "a single file to import it.",
            download: "Download a file",
            delete: "Delete a file",
        }
    },
    resource: {
        name: "Resource",
        download: "Download",
        upload: "Upload",
        new: "Add a resource",
        store: "Store",
        cancel: "Cancel",
        types: {
            markdown: "MarkDown",
            download: "Download",
            weblink: "Web link",
        },
        field: {
            title: "Title",
            type: "Type",
            description: "Description",
            content: "Content",
        },
    },
    comment: {
        name: "Comments",
        placeholder: "Add your comment",
        close: "Close",
        empty: "Nothing right now. Once your study teams start becoming active, you should see comments here.",
    },
    search: {
        name: "Search",
        empty: "Search for study teams for their study pathways.",
    },
    frontpage: {
        title: "The Global Health Network Study Builder",
        description: "The collaborative global health research study builder and support companion",
        tghnFull: "The Global Health Network",
        tghn: "TGHN",
        getstarted: "Get started",
        learnmore: "Learn more",
        pathwayTitle: "Study pathways",
        groupTitle: "Featured studies",
        steps: {
            one: "Create account",
            two: "Complete personal profile",
            three: "Create study pathway as an individual, for a team, or join an existing team",
            four: "Invite team members, or complete a study pathway on your own",
        },
    },
    errorpage: {
        error: "404 error",
        description: "Sorry, something went wrong. This page isn't available.",
        gohome: "Go back home",
    },
    loginpage: {
        submit: "Submit",
        login: {
            titleEmail: "Login with email",
            titlePassword: "Login with password",
            descriptionEmail: "We'll check if you have an account, and create one if you don't.",
            descriptionPassword: "You'll need to have set a password in your settings after first creating an account.",
            emailLabel: "Email address",
            passwordLabel: "Password",
            passwordForgot: "Forgot your password?",
            passwordPrefer: "If you prefer, use your password & don't email.",
        },
        magic: {
            title: "Check your email",
            description1: "We sent you an email with a magic link. Once you click that (or copy it into this browser) you'll be signed in.",
            description2: "Make sure you use the same browser you requested the login from or it won't work.",
            alternative: "If you prefer, use your password & don't email.",
        },
        recover: {
            title: "Recover your account",
            emailLabel: "Email address",
            login: "Login to your account",
        },
        reset: {
            title: "Reset your password",
            passwordLabel: "Password",
            passwordConfirm: "Repeat password",
        },
        totp: {
            title: "Two-factor authentication",
            description: "Enter the 6-digit verification code from your app.",
            label: "Verification code",
        },
    },
    pwa: {
        dismiss: "Dismiss",
        install: "Install",
        install_title: "Install TGHN",
        title: "New TGHN update available!",
        update: "Update",
        update_available_short: "Update TGHN",
    },
}